import math

def calculate_gypsum_ball_specs(outer_diameter_cm, wall_thickness_mm):
    # Convert measurements to centimeters
    R_outer = outer_diameter_cm / 2.0
    wall_thickness_cm = wall_thickness_mm / 10.0
    R_inner = R_outer - wall_thickness_cm
    
    # Sphere volume formula: (4/3) * pi * r^3
    volume_outer_l = ((4.0 / 3.0) * math.pi * (R_outer ** 3)) / 1000.0
    volume_inner_l = ((4.0 / 3.0) * math.pi * (R_inner ** 3)) / 1000.0
    
    # Gypsum material volume in liters
    gypsum_volume_l = volume_outer_l - volume_inner_l
    
    print(f"--- ONE DROP OASIS: GYPSUM BALL TECHNICAL SPECS ---")
    print(f"Outer Diameter: {outer_diameter_cm} cm")
    print(f"Wall Thickness: {wall_thickness_mm} mm")
    print(f"----------------------------------------------------")
    print(f"✓ Internal nutrient volume (biomass): {volume_inner_l:.2f} liters (~6L)")
    print(f"✓ Required gypsum material: {gypsum_volume_l:.2f} liters per ball")
    print(f"✓ Total displaced volume in soil: {volume_outer_l:.2f} liters")
    print(f"----------------------------------------------------")
    print(f"Mechanical Advantage: Saves {((volume_inner_l/volume_outer_l)*100):.1f}% material compared to a solid sphere.")

# Run calculations with the optimized specifications (25cm diameter, 12mm wall)
calculate_gypsum_ball_specs(25.0, 12.0)
