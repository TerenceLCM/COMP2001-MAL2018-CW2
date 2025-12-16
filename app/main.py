from fastapi import FastAPI
from app.database import get_connection
from fastapi import Header, HTTPException
from typing import Optional
from fastapi import Body
from fastapi import HTTPException

app = FastAPI(
    title="Trail Service API",
    description="Micro-service for managing hiking trails",
    version="1.0.0"
)

@app.get("/", tags = ["System"])
def root():
    return {"status": "TrailService running"}

@app.get("/trails", tags =["Trails"])
def get_trails():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.Trail_ID,
            t.Trail_Name,
            t.Description,
            c.Category_Name,
            d.Difficulty_Name,
            r.Route_Type
        FROM CW2.Trail t
        JOIN CW2.Category c ON t.Category_ID = c.Category_ID
        JOIN CW2.Difficulty d ON t.Difficulty_ID = d.Difficulty_ID
        JOIN CW2.Route_Type r ON t.Route_ID = r.Route_ID
    """)

    trails = []
    for row in cursor.fetchall():
        trails.append({
            "trail_id": row.Trail_ID,
            "trail_name": row.Trail_Name,
            "description": row.Description,
            "category": row.Category_Name,
            "difficulty": row.Difficulty_Name,
            "route_type": row.Route_Type
        })

    conn.close()
    return trails

@app.get("/trails/{trail_id}", tags =["Trails"])
def get_trail_by_id(trail_id: int, x_user_id: Optional[int] = Header(None)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.Trail_ID,
            t.Trail_Name,
            t.Description,
            t.Distance,
            t.Elevation_Gain,
            t.Estimate_Time,
            t.Trail_Info,
            t.User_ID,
            c.Category_Name,
            d.Difficulty_Name,
            r.Route_Type
        FROM CW2.Trail t
        JOIN CW2.Category c ON t.Category_ID = c.Category_ID
        JOIN CW2.Difficulty d ON t.Difficulty_ID = d.Difficulty_ID
        JOIN CW2.Route_Type r ON t.Route_ID = r.Route_ID
        WHERE t.Trail_ID = ?
    """, trail_id)

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Trail not found")

    is_owner = x_user_id is not None and x_user_id == row.User_ID

    # Public (limited) view
    trail = {
        "trail_id": row.Trail_ID,
        "trail_name": row.Trail_Name,
        "category": row.Category_Name,
        "difficulty": row.Difficulty_Name,
        "route_type": row.Route_Type
    }

    # Owner gets full view
    if is_owner:
        trail.update({
            "description": row.Description,
            "distance": row.Distance,
            "elevation_gain": row.Elevation_Gain,
            "estimate_time": row.Estimate_Time,
            "trail_info": row.Trail_Info
        })

    return trail

@app.get("/trails/{trail_id}/points", tags =["Trail Points"])
def get_trail_points(trail_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Point_ID,
            Latitude,
            Longitude,
            PointOrder
        FROM CW2.Trail_Point
        WHERE Trail_ID = ?
        ORDER BY PointOrder
    """, trail_id)

    points = []
    for row in cursor.fetchall():
        points.append({
            "point_id": row.Point_ID,
            "latitude": float(row.Latitude),
            "longitude": float(row.Longitude),
            "order": row.PointOrder
        })

    conn.close()
    return points

@app.get("/trails/{trail_id}/features", tags =["Features"])
def get_trail_features(trail_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.Feature_ID,
            f.Feature_Name,
            f.Feature_Description
        FROM CW2.Trail_Feature tf
        JOIN CW2.Feature f ON tf.Feature_ID = f.Feature_ID
        WHERE tf.Trail_ID = ?
    """, trail_id)

    features = []
    for row in cursor.fetchall():
        features.append({
            "feature_id": row.Feature_ID,
            "feature_name": row.Feature_Name,
            "feature_description": row.Feature_Description
        })

    conn.close()
    return features

@app.post("/trails", tags =["Trails"])
def create_trail(
    trail: dict = Body(...),
    x_user_id: Optional[int] = Header(None)
):
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO CW2.Trail (
            Trail_Name,
            Description,
            Distance,
            Elevation_Gain,
            Estimate_Time,
            Trail_Info,
            Category_ID,
            Difficulty_ID,
            Route_ID,
            User_ID
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trail["trail_name"],
        trail.get("description"),
        trail.get("distance"),
        trail.get("elevation_gain"),
        trail.get("estimate_time"),
        trail.get("trail_info"),
        trail["category_id"],
        trail["difficulty_id"],
        trail["route_id"],
        x_user_id
    ))

    conn.commit()
    conn.close()

    return {"message": "Trail created successfully"}

@app.put("/trails/{trail_id}", tags =["Trails"])
def update_trail(trail_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE CW2.Trail
        SET Trail_Name = ?, Distance = ?
        WHERE Trail_ID = ?
    """, data.get("trail_name"), data.get("distance"), trail_id)

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Trail not found")

    conn.commit()
    conn.close()
    return {"message": "Trail updated successfully"}

@app.delete("/trails/{trail_id}", tags =["Trails"])
def delete_trail(trail_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM CW2.Trail
        WHERE Trail_ID = ?
    """, trail_id)

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Trail not found")

    conn.commit()
    conn.close()
    return {"message": "Trail deleted successfully"}