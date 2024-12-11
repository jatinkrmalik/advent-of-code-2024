import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

def create_topographic_visualizations(grid, output_prefix="topo"):
    """
    Create multiple visualizations of the topographic map.
    
    Args:
        grid: 2D numpy array of heights
        output_prefix: prefix for saving output files
    """
    # Convert grid to numpy array if it isn't already
    grid = np.array(grid)
    
    # Set up the figure size and DPI for high quality
    plt.figure(figsize=(12, 8), dpi=300)
    
    # Style 1: Heatmap with contours
    plt.subplot(221)
    plt.title("Heatmap with Contours")
    # Create contour plot
    contour = plt.contour(grid, levels=np.arange(0, 10, 1), colors='black', alpha=0.3)
    # Add colored heatmap
    plt.imshow(grid, cmap='terrain')
    plt.colorbar(label='Height')
    plt.clabel(contour, inline=True, fontsize=8)
    
    # Style 2: 3D Surface Plot
    ax = plt.subplot(222, projection='3d')
    plt.title("3D Surface")
    x, y = np.meshgrid(np.arange(grid.shape[1]), np.arange(grid.shape[0]))
    surf = ax.plot_surface(x, y, grid, cmap='terrain', 
                          linewidth=0, antialiased=True)
    plt.colorbar(surf, label='Height')
    ax.view_init(elev=45, azim=45)
    
    # Style 3: Filled Contour Plot
    plt.subplot(223)
    plt.title("Filled Contour Plot")
    plt.contourf(grid, levels=np.arange(0, 10, 0.5), cmap='terrain')
    plt.colorbar(label='Height')
    
    # Style 4: Topographic Lines Only
    plt.subplot(224)
    plt.title("Topographic Lines")
    plt.contour(grid, levels=np.arange(0, 10, 0.5), 
                colors='black', linewidths=0.5)
    plt.imshow(grid, cmap='gray', alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_combined.png", bbox_inches='tight', dpi=300)
    plt.close()
    
    # Create individual high-resolution plots
    
    # 3D Surface with different viewing angles
    fig = plt.figure(figsize=(12, 12), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, grid, cmap='terrain', 
                          linewidth=0, antialiased=True)
    plt.colorbar(surf, label='Height')
    ax.view_init(elev=30, azim=45)
    plt.savefig(f"{output_prefix}_3d_surface.png", bbox_inches='tight', dpi=300)
    plt.close()
    
    # Detailed contour map
    plt.figure(figsize=(12, 12), dpi=300)
    plt.contour(grid, levels=np.arange(0, 10, 0.2), 
                colors='black', linewidths=0.5)
    plt.contourf(grid, levels=np.arange(0, 10, 0.2), 
                 cmap='terrain', alpha=0.7)
    plt.colorbar(label='Height')
    plt.title("Detailed Topographic Map")
    plt.savefig(f"{output_prefix}_detailed_contour.png", 
                bbox_inches='tight', dpi=300)
    plt.close()

# Example usage with test data
def create_sample_visualization():
    """
    Create a sample visualization using test data from the puzzle
    """
    # Sample grid from the puzzle
    test_grid = """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    
    # Convert string to numpy array
    grid = np.array([[int(c) for c in line.strip()] 
                     for line in test_grid.strip().split('\n')])
    
    # Create visualizations
    create_topographic_visualizations(grid, "sample_topo")

if __name__ == "__main__":
    # Create sample visualization
    create_sample_visualization()
    
    # If you have your input file:
    try:
        with open('input.txt', 'r') as f:
            grid = np.array([[int(c) for c in line.strip()] 
                            for line in f.readlines()])
            create_topographic_visualizations(grid, "puzzle_topo")
    except FileNotFoundError:
        print("input.txt not found, only sample visualization created")
