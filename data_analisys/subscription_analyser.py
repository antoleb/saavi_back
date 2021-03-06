import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression


from data_analisys import paths


class SubscribtionAnalyser:
    def __init__(self):
        self.data = pd.read_csv(paths.subscription_dataset_path, sep=';')
        self.data.at[1057, 'date_of_payment'] = 9
        self.data.at[1061, 'date_of_payment'] = 10
        ohe = OneHotEncoder()

        one_hot_features = ohe.fit_transform(self.data[['service_name', 'service_category']]).toarray()
        one_hot_features *= self.data.number_of_payments.values[:, None]

        features = np.concatenate([self.data.user_id.values[:, None], one_hot_features], 1)
        features = pd.DataFrame(features, columns=['user_id'] + list(ohe.get_feature_names()))

        self.model_dict = {}
        self.service_category_dict = {}
        for service_name in self.data.service_name.unique():
            service_mask = self.data.service_name != service_name
            self.service_category_dict[service_name] = self.data[~service_mask].service_category.values[0]
            train_features = features[service_mask]
            train_features = train_features.groupby('user_id').sum()
            prediction_users = self.data.user_id[~service_mask].unique()
            train_y = np.isin(train_features.index, prediction_users)
            model = LogisticRegression(max_iter=1e7, class_weight='balanced', C=1e-2)
            model.fit(train_features, train_y)
            self.model_dict[service_name] = model
        self.features = features

    def predict_user(self, val_user, n=5):
        key_list = []
        prediction_list = []
        for key, item in self.model_dict.items():
            service_mask = self.data.service_name != key
            train_features = self.features[service_mask]
            train_features = train_features.groupby('user_id').sum()

            prediction_users = self.data.user_id[~service_mask].unique()
            if val_user in prediction_users:
                continue

            inputs = train_features.loc[val_user].values[None]
            key_list.append(key)
            prediction_list.append(item.predict_proba(inputs)[0, 1])

        sort = np.argsort(prediction_list)[::-1]
        key_list = np.array(key_list)
        prediction_list = np.array(prediction_list)
        return [
            {
                'service_name': key,
                'score': prediction_score,
                'service_category':self.service_category_dict[key]
            } for key, prediction_score in zip(key_list[sort][:n], prediction_list[sort][:n])
        ]

    def get_active_subscriptions(self, val_user):
        user_slice = self.data[self.data.user_id == val_user]
        result_list = [
            {
                'service name': user_slice.iloc[i].service_name,
                'service category': user_slice.iloc[i].service_category,
                'amount': (user_slice.iloc[i].price_min + user_slice.iloc[i].price_max) / 2,
                'is_avarage': str(user_slice.iloc[i].price_min != user_slice.iloc[i].price_max),
                'next_payment_date': int(user_slice.iloc[i].date_of_payment),
                'total_spend': (user_slice.iloc[i].number_of_payments *
                                (user_slice.iloc[i].price_min + user_slice.iloc[i].price_max) / 2),
                'next_charge': f'{2020}-{11 + (user_slice.iloc[i].date_of_payment < 8)}-{user_slice.iloc[i].date_of_payment}'
            }
            for i in range(user_slice.shape[0])
        ]
        argsort = np.argsort([res['total_spend'] for res in result_list])[::-1]
        return [result_list[i] for i in argsort]

    def get_next_two_subscriptions(self, val_user, current_day):
        active_subscriptions = self.get_active_subscriptions(val_user)
        if len(active_subscriptions) >= 2:
            next_subscriptions_date_list = []
            for sub in active_subscriptions:
                next_subscriptions_date_list.append(int(sub['next_payment_date']) + 200 * (int(sub['next_payment_date']) < current_day))
            sort = np.argsort(next_subscriptions_date_list)
            return [active_subscriptions[sort[0]], active_subscriptions[sort[1]]]
        return active_subscriptions

    def get_month_subscription_payment(self, val_user):
        active_subscriptions = self.get_active_subscriptions(val_user)
        return sum([active_subscription['amount'] for active_subscription in active_subscriptions])