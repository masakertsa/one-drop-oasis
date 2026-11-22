"""
One Drop Oasis - Calculation Framework
Parametric thermodynamic, material dissolution, and biological nutrient release model
for the passive anti-desertification module (bamboo dew condenser + 6L gypsum sphere).
"""

import math


def calculate_dew_point(ambient_temp_c: float, relative_humidity_pct: float) -> float:
    """
    Calculates the dew point temperature (in Celsius) using the Magnus-Tetens formula.
    
    Parameters:
    - ambient_temp_c (float): Ambient desert air temperature in Celsius.
    - relative_humidity_pct (float): Relative humidity in % (0-100).
    
    Returns:
    - float: Dew point temperature in Celsius.
    """
    if relative_humidity_pct <= 0:
        return -273.15

    rh = min(100.0, relative_humidity_pct)
    a = 17.27
    b = 237.7

    alpha = ((a * ambient_temp_c) / (b + ambient_temp_c)) + math.log(rh / 100.0)
    dew_point_c = (b * alpha) / (a - alpha)
    return round(dew_point_c, 2)


def estimate_nightly_water_yield(
    pipe_surface_area_m2: float,
    night_air_temp_c: float,
    night_humidity_pct: float,
    radiative_cooling_drop_c: float = 4.5,
) -> float:
    """
    Estimates passive nightly water condensation yield (in liters) inside and along
    the vertical hollow bamboo condenser pipe during diurnal desert temperature drops.
    """
    if pipe_surface_area_m2 <= 0 or night_humidity_pct <= 0:
        return 0.0

    dew_point_c = calculate_dew_point(night_air_temp_c, night_humidity_pct)
    pipe_surface_temp_c = night_air_temp_c - radiative_cooling_drop_c

    # Condensation triggers when radiative cooling drops pipe wall temperature below dew point
    subcooling_delta_c = dew_point_c - pipe_surface_temp_c
    if subcooling_delta_c <= 0:
        return 0.0

    # Empirical passive radiative/convective dew yield (~0.085 L / m^2 per °C below dew point)
    condensation_coeff_l_m2_c = 0.085
    nightly_yield_liters = pipe_surface_area_m2 * subcooling_delta_c * condensation_coeff_l_m2_c
    return round(nightly_yield_liters, 4)


def model_gypsum_dissolution_rate(
    soil_moisture_pct: float,
    surface_sand_temp_c: float,
    wall_thickness_mm: float = 12.0,
    burial_depth_cm: float = 40.0,
) -> float:
    """
    Models the slow-release structural lifespan (in months) of the 12 mm calcium sulfate
    (gypsum) sphere shell at 40 cm burial depth.
    """
    if soil_moisture_pct <= 0 or wall_thickness_mm <= 0:
        return 0.0

    # At 40 cm depth under basalt mulch, thermal damping reduces extreme surface heat spikes
    depth_damping = math.exp(-burial_depth_cm / 35.0)
    subsurface_temp_c = 26.0 + (surface_sand_temp_c - 26.0) * depth_damping

    # Baseline dissolution rate (~0.65 mm/month at 10% moisture and 28°C subsurface temp)
    moisture_factor = soil_moisture_pct / 10.0
    kinetic_temp_factor = 1.0 + 0.015 * (subsurface_temp_c - 28.0)

    dissolution_rate_mm_per_month = max(0.15, 0.65 * moisture_factor * kinetic_temp_factor)
    lifespan_months = wall_thickness_mm / dissolution_rate_mm_per_month
    return round(lifespan_months, 1)


def simulate_npk_payload_release(
    months_active: float,
    total_payload_liters: float = 6.0,
    shell_lifespan_months: float = 18.0,
) -> dict:
    """
    Tracks the controlled cumulative release (in liters and %) of the 6-liter sterilized
    organic NPK biomass payload into the deep 40 cm root zone.
    """
    if months_active <= 0 or shell_lifespan_months <= 0:
        return {"released_liters": 0.0, "released_pct": 0.0, "remaining_liters": total_payload_liters}

    # Sigmoidal release curve: slow initial diffusion through gypsum pores, accelerating as shell thins
    progress_ratio = min(1.5, months_active / shell_lifespan_months)
    release_fraction = min(1.0, 1.0 / (1.0 + math.exp(-6.0 * (progress_ratio - 0.55))))

    released_liters = total_payload_liters * release_fraction
    remaining_liters = max(0.0, total_payload_liters - released_liters)

    return {
        "released_liters": round(released_liters, 2),
        "released_pct": round(release_fraction * 100.0, 1),
        "remaining_liters": round(remaining_liters, 2),
    }


if __name__ == "__main__":
    print("--- One Drop Oasis: Calculation Framework ---")

    # 1. Desert night conditions: 14°C air temp, 78% relative humidity
    dp = calculate_dew_point(14.0, 78.0)
    print(f"1. Desert Night Dew Point (14°C, 78% RH): {dp} °C")

    # 2. Nightly water yield for a 0.35 m^2 bamboo condenser array
    yield_l = estimate_nightly_water_yield(pipe_surface_area_m2=0.35, night_air_temp_c=14.0, night_humidity_pct=78.0)
    print(f"2. Estimated Nightly Water Condensation: {yield_l} liters/night ({yield_l * 30:.2f} L/month)")

    # 3. 12 mm gypsum ball dissolution at 40 cm depth (60°C surface sand, 8% subsurface moisture)
    lifespan = model_gypsum_dissolution_rate(soil_moisture_pct=8.0, surface_sand_temp_c=60.0, wall_thickness_mm=12.0)
    print(f"3. 12mm Gypsum Sphere Structural Lifespan: {lifespan} months")

    # 4. 6-liter organic NPK payload release at Month 12
    npk = simulate_npk_payload_release(months_active=12.0, total_payload_liters=6.0, shell_lifespan_months=lifespan)
    print(f"4. 6L NPK Payload at Month 12: {npk['released_liters']} L released ({npk['released_pct']}%)")
