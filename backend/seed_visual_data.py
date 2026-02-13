from app import create_app, db
from app.models import WorkingFace, DrillingSite, Borehole, BoreholeTrajectory, FractureConstructionData, MicroseismicEvent
from datetime import datetime, timedelta
import random
import math

app = create_app()

def seed_visual_data():
    with app.app_context():
        # 1. Clear existing data
        BoreholeTrajectory.query.delete()
        FractureConstructionData.query.delete()
        Borehole.query.delete()
        DrillingSite.query.delete()
        WorkingFace.query.delete()
        MicroseismicEvent.query.delete()
        db.session.commit()

        # 2. Create Working Face 11223
        wf = WorkingFace(
            name='11223工作面',
            length=260.0,
            advance_length=1500.0,
            mining_height=3.5,
            start_date=datetime(2025, 1, 1),
            description='小纪汗煤矿11223主采面'
        )
        db.session.add(wf)
        db.session.commit()

        # 3. Create 5 Drilling Sites (28, 25, 14, 7, 1 联巷)
        sites_info = [
            {'name': '28联巷钻场', 'e': 35400.0, 'n': 28000.0, 'z': -610.0},
            {'name': '25联巷钻场', 'e': 35400.0, 'n': 28150.0, 'z': -612.0},
            {'name': '14联巷钻场', 'e': 35400.0, 'n': 28450.0, 'z': -615.0},
            {'name': '7联巷钻场', 'e': 35400.0, 'n': 28750.0, 'z': -618.0},
            {'name': '1联巷钻场', 'e': 35400.0, 'n': 28950.0, 'z': -620.0},
        ]

        for s in sites_info:
            site = DrillingSite(
                working_face_id=wf.id,
                name=s['name'],
                location=s['name'],
                coord_e=s['e'],
                coord_n=s['n'],
                coord_z=s['z']
            )
            db.session.add(site)
            db.session.flush()

            # 4. Create 6 Boreholes per site
            for i in range(1, 7):
                # Design parameters
                azimuth = 270.0 + (i - 3.5) * 5  # Fan shape
                dip = 10.0 + random.random() * 5
                length = 500.0 + random.random() * 100

                bh = Borehole(
                    drilling_site_id=site.id,
                    borehole_no=f'HF-{site.name[:2]}-{i:02d}',
                    diameter=96.0,
                    design_length=length,
                    azimuth=azimuth,
                    dip_angle=dip,
                    segments=12
                )
                db.session.add(bh)
                db.session.flush()

                # 5. Create Trajectories (Actual vs Design simulation)
                points_count = 10
                for j in range(points_count + 1):
                    md = (length / points_count) * j
                    
                    # Calculate actual position with some deviation
                    rad_az = math.radians(azimuth + (random.random() - 0.5) * 2)
                    rad_dip = math.radians(dip + (random.random() - 0.5) * 1)
                    
                    dist_h = md * math.cos(rad_dip)
                    de = dist_h * math.sin(rad_az)
                    dn = dist_h * math.cos(rad_az)
                    dz = md * math.sin(rad_dip)

                    traj = BoreholeTrajectory(
                        borehole_id=bh.id,
                        measured_depth=md,
                        dip_angle=math.degrees(rad_dip),
                        grid_azimuth=math.degrees(rad_az),
                        coord_e=site.coord_e + de,
                        coord_n=site.coord_n + dn,
                        coord_z=site.coord_z + dz,
                        timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
                    )
                    db.session.add(traj)

                # 6. Seed Fracture Data for some segments
                for seg in range(1, random.randint(3, 8)):
                    frac = FractureConstructionData(
                        borehole_id=bh.id,
                        segment_no=seg,
                        pressure=20.0 + random.random() * 15.0,
                        flow_rate=1.5 + random.random() * 1.0,
                        total_volume=80.0 + random.random() * 40.0,
                        record_time=datetime.now() - timedelta(days=random.randint(0, 5))
                    )
                    db.session.add(frac)

        # 7. Seed some Microseismic Events
        for _ in range(100):
            ms = MicroseismicEvent(
                event_time=datetime.now() - timedelta(hours=random.randint(0, 720)),
                coord_x=35300 + random.random() * 200,
                coord_y=28000 + random.random() * 1000,
                coord_z=-600 + random.random() * 30,
                energy=random.randint(100, 50000)
            )
            db.session.add(ms)

        db.session.commit()
        print("Visualization seed data created successfully!")

if __name__ == "__main__":
    seed_visual_data()
