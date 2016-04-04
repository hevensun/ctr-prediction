
# Following: https://dato.com/learn/gallery/notebooks/feature_engineering_with_graphlab_create.html

########################################################################################################################

# import package
import graphlab as gl

########################################################################################################################

# load train data
data = gl.SFrame.read_csv('data/train_data.txt', delimiter='\t', verbose=False)
# split train data to train set and validation set
train_set, validation_set = data.random_split(0.8, seed=1)

# get features
features = data.column_names()
# remove click label feature
features.remove('click')

# remove some features temporarily
features.remove('ip')
features.remove('url')
features.remove('domain')
features.remove('user_id')
features.remove('log_type')
features.remove('timestamp')
features.remove('user_tags')
features.remove('ad_slot_id')
features.remove('creative_id')
features.remove('key_page_url')
features.remove('advertiser_id')
features.remove('anonymous_url_id')

# for checking features
# print(features)

########################################################################################################################

# baseline logistic regression model - uses all features
log_baseline = gl.logistic_classifier.create(train_set, target='click', features=features,
                                             validation_set=validation_set, max_iterations=50)

# calculate logistic regression model validation set auc
log_auc = log_baseline.evaluate(validation_set, metric='auc')

# print logistic regression model validation set auc
print 'Logistic Regression Model - Validation Set - AUC: {}\n'.format(log_auc)

# load test data
test_data = gl.SFrame.read_csv('data/test_data.txt', delimiter='\t', verbose=False)

# get logistic regression model predictions
log_predictions = log_baseline.predict(test_data, output_type='probability')

########################################################################################################################

# open logistic regression model predictions file
with open('predictions/log_predictions.csv', mode='w') as log_prediction_file:
    # write headers to file
    log_prediction_file.write('Id,Prediction\n')
    # set logistic regression model prediction id to 1
    log_prediction_id = 1
    # for every logistic regression model prediction
    for log_prediction in log_predictions:
        # write logistic regression model prediction to file in requested format
        log_prediction_file.write('{},{:.5f}\n'.format(log_prediction_id, log_prediction))
        # increment logistic regression model prediction id
        log_prediction_id += 1

# close logistic regression model predictions file
log_prediction_file.close()

########################################################################################################################
