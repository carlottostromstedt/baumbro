import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import math

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
            if decoded == "GPSInfo":
                gps_info = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
                exif_data[decoded] = gps_info
    return exif_data

def get_gps_info(image_path):
    with Image.open(image_path) as img:
        exif_data = get_exif_data(img)
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                latitude = gps_info["GPSLatitude"]
                longitude = gps_info["GPSLongitude"]
                return latitude, longitude
    return None, None

def convert_to_decimal_degrees(coord):
    degrees, minutes, seconds = coord
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    return decimal_degrees

def get_coordinates(picture_file):
        img = Image.open(picture_file)
        img_exif = img.getexif()
        print(img_exif)
        print(get_gps_info(picture_file))
        latitude, longitude = get_gps_info(picture_file)
        latitude_decimal = convert_to_decimal_degrees(latitude)
        longitude_decimal = convert_to_decimal_degrees(longitude)

        print("Latitude (Decimal Degrees):", latitude_decimal)
        print("Longitude (Decimal Degrees):", longitude_decimal)
        # <class 'PIL.Image.Exif'>
        if img_exif is None:
            print('Sorry, image has no exif data.')
        else:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    print(f'{ExifTags.TAGS[key]}:{val}')
                else:
                    print(f'{key}:{val}')
        return longitude_decimal, latitude_decimal

def calculate_query_values(longitude: float, latitude: float, distance: int) -> dict:
  # Earth's mean radius in meters
  earth_radius = 6371000

  # Conversion factor from degrees to meters
  degrees_to_meters = earth_radius * math.pi / 180

  # Calculate the delta in degrees based on distance
  delta_degrees = distance / degrees_to_meters

  # Calculate minimum and maximum latitudes
  min_latitude = latitude - delta_degrees
  max_latitude = latitude + delta_degrees

  # Calculate minimum and maximum longitudes considering latitude for accurate distance calculation
  min_longitude = longitude - delta_degrees / math.cos(math.radians(latitude))
  max_longitude = longitude + delta_degrees / math.cos(math.radians(latitude))

  # Create a dictionary to store the results
  max_min_values = {
      "minLongitude": min_longitude,
      "maxLongitude": max_longitude,
      "minLatitude": min_latitude,
      "maxLatitude": max_latitude
  }

  return max_min_values