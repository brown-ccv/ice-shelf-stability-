def main():
    """
    Main function to execute the water coverage calculation and print the results.
    """
    shapefile_path = '/Users/chollid1/Desktop/TimeLine_Shapefiles_gl/2015_08-07.shp'
    binary_image_path = '/Users/chollid1/Desktop/Water_coverage Geotiff/2015_08-07_GeoTiff.tif'

    water_coverage_percent = calculate_water_coverage(shapefile_path, binary_image_path)
    if water_coverage_percent is not None:
        print(f"Water coverage within ice shelf boundary: {water_coverage_percent:.2f}%")

"""
    Calculates the percentage of water coverage within the ice shelf boundary based on a shapefile and GeoTIFF.
    
    Parameters:
        shapefile_path (str): Path to the shapefile containing the ice shelf boundary.
        binary_image_path (str): Path to the binary GeoTIFF image where 0 represents water.
    
    Returns:
        float: Percentage of water coverage within the ice shelf boundary.
    """

import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import numpy as np

def calculate_water_coverage(shapefile_path, binary_image_path):
    
    try:
        """
        Read shapefile using geopandas
        """
        ice_shelf_boundary = gpd.read_file(shapefile_path)

        """
        Open GeoTIFF using rasterio
        """
        with rasterio.open(binary_image_path) as src:
            """
            Read image as numpy array using first band of raster data
            """
            binary_image = src.read(1)
            
            """
            Gets transformation to relate pixel coordinates to geographic coordinates
            """
            transform = src.transform
            
            """
            Rasterize the ice shelf boundary to create a mask. Sets the ice shelf boundary to true
            and everything else outside boundary to false.
            """
            ice_shelf_mask = geometry_mask(
                ice_shelf_boundary.geometry,
                out_shape=binary_image.shape,
                transform=transform,
                invert=True
            )
            
            """
            Apply the mask to the binary image to get pixels within the ice shelf boundary
            """
            water_pixels_in_boundary = binary_image[ice_shelf_mask]
        
        """
        Calculate the percentage of water coverage.
        total_pixels_within_boundary: number of pixels in the ice shelf boundary
        water_pixels_in_boundary_count: number of water pixels in the ice shelf boundary
        """
        total_pixels_within_boundary = water_pixels_in_boundary.size
        water_pixels_in_boundary_count = (water_pixels_in_boundary == 0).sum()

        """
        Calculates % of water pixels out of the total number of pixels
        """
        if total_pixels_within_boundary > 0:
            water_coverage_percent = (water_pixels_in_boundary_count / total_pixels_within_boundary) * 100
        else:
            # Handle case when no pixels are within the boundary
            water_coverage_percent = 0.0 

        return water_coverage_percent
    except Exception as e:
        """
        Handles errors and prints error message
        """
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    main()
