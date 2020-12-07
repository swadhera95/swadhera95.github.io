## Sidhant Wadhera
## R Code Sample 

# This sample reads in a processed dataset that combines statewide election results with 
# polling, political, and economic fundamentals. These data are then used to fit a simple
# linear model predicting the Democratic two-party vote share in previous elections. The
# script proceeds to conduct a six-fold cross validation and returns various model metrics. 
# This sample comes from code written as part of an assignment for The Science of Elections
# and Campaigns, taken in the Autumn of 2020. 

library(caret) 
library(dplyr)

set.seed(13608)

ModelValidation <- function(model, df){
  train_control <- trainControl(method = 'cv', number = 6)
  validation <- train(formula(model$call[[2]]), data = df, trControl = train_control, method = 'lm')
  return(validation)
}

load('modeling_df.rdata')

modelingdf_nomiss <- modeling_df %>%
  tidyr::drop_na()

# Outcome: Dem 2 Party Vote Share
# Regressors: Dem 2 Party Poll Share, Previous Cycle Vote Share, Democratic Incumbent, Incumbent Running, 
#             State Partisanship, Unemployment Rate, Interaction Term

pred_model <- lm(dem_2p_vs ~ dem_2p_ps + prv_2p_vs + deminc + incrunning + st_partisanship + unemp_rate + deminc:incrunning, 
                 data = modelingdf_nomiss)
summary(pred_model)

validation <- ModelValidation(pred_model, modelingdf_nomiss)
print(validation)