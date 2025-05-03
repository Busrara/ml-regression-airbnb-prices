# ml-regression-house-prices

This is is a machine learning-based regression model project that can predict housing prices using various property features. It uses the Random Forest Regressor algorithm and visualizes feature importance to achieve better interpretability.

## Dataset

The dataset includes real estate listings with several features, such as:
- Area (in square meters)
- Number of rooms
- Age of the building
- Floor level
- Neighborhood
- Heating type
- Building type
- Furnishing status
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
