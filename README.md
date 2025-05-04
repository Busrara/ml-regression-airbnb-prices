# ml-regression-airbnb-prices

This is is a machine learning-based regression model project that can predict Airbnb housing prices using various property features. It uses the Random Forest Regressor algorithm and visualizes feature importance to achieve better interpretability.

## Dataset

The dataset includes listings with several features, such as:
- Room type
- Longtitude
- Age of the building
- Number of Reviews
- Latitude
- Minimum nights
- And more...

## Workflow

1. **Data Cleaning**: 
   - Handled outliers based on quantile thresholds.
   - Removed duplicate and irrelevant rows.

2. **Feature Engineering**:
   - Converted categorical variables using one-hot encoding.
   - Dropped unnecessary columns.

3. **Modeling**:
   - Used `RandomForestRegressor`.
   - Evaluated using RMSE and R².

4. **Visualization**:
   - Visualized feature importances with Seaborn for better interpretability.

Read my Medium writing on this project to have a deeper understanding: https://medium.com/@busraracoban/from-data-to-value-building-a-house-price-prediction-model-in-python-4c15a68561d6?postPublishedType=initial
