import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify as mc

# Load example data (replace with your data)
# Example data can be found in the GeoPandas documentation
gdf = gpd.read_file(gpd.datasets.available_maps['nybb'])
data_column = 'Shape_Area'

# 1. Calculate global vmin and vmax across all data points
global_vmin = gdf[data_column].min()
global_vmax = gdf[data_column].max()

# Define classification schemes to compare
schemes = ['equal_interval', 'quantiles', 'natural_breaks']

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)

for ax, scheme in zip(axs, schemes):
    # Create the choropleth map using the specified scheme
    # CRITICAL: Use the global vmin and vmax to fix the color range
    gdf.plot(
        column=data_column,
        scheme=scheme,
        cmap='viridis',
        vmin=global_vmin,  # Use global min
        vmax=global_vmax,  # Use global max
        legend=True,
        ax=ax,
        k=5, # Number of classes (bins)
        linewidth=0.8,
        edgecolor='0.8'
    )
    ax.set_title(f'{scheme.replace("_", " ").title()} Classification')
    ax.axis('off')

plt.suptitle('Choropleth Maps with Different Classification Methods (Fixed Color Range)', y=1.05)
plt.show()
