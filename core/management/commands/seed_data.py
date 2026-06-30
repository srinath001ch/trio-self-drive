import io
import random

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from cars.models import Car
from core.models import FAQ, Testimonial

User = get_user_model()


CAR_DATA = [
    ("Maruti Suzuki", "Swift", "VXi 2023", 1200, Car.FUEL_PETROL, Car.TRANSMISSION_MANUAL, 5, "22 km/l",
     "A peppy and fuel-efficient hatchback, perfect for city driving and quick getaways."),
    ("Hyundai", "Creta", "SX 2023", 2500, Car.FUEL_DIESEL, Car.TRANSMISSION_AUTOMATIC, 5, "18 km/l",
     "A stylish and spacious SUV with a comfortable cabin, ideal for family trips."),
    ("Toyota", "Innova Crysta", "ZX 2022", 3200, Car.FUEL_DIESEL, Car.TRANSMISSION_MANUAL, 7, "14 km/l",
     "A reliable 7-seater perfect for long road trips and large groups."),
    ("Maruti Suzuki", "Baleno", "Zeta 2023", 1300, Car.FUEL_PETROL, Car.TRANSMISSION_AUTOMATIC, 5, "21 km/l",
     "A premium hatchback offering a smooth ride with modern features."),
    ("Mahindra", "Thar", "LX 2023", 2800, Car.FUEL_DIESEL, Car.TRANSMISSION_MANUAL, 4, "15 km/l",
     "A rugged off-roader for adventure lovers who want to explore beyond the city."),
    ("Hyundai", "i20", "Sportz 2023", 1400, Car.FUEL_PETROL, Car.TRANSMISSION_MANUAL, 5, "20 km/l",
     "A sporty hatchback with a punchy engine and premium interiors."),
    ("Kia", "Seltos", "HTX 2023", 2600, Car.FUEL_PETROL, Car.TRANSMISSION_AUTOMATIC, 5, "16 km/l",
     "A bold compact SUV with advanced features and a commanding road presence."),
    ("Tata", "Nexon EV", "XZ Plus 2023", 2200, Car.FUEL_ELECTRIC, Car.TRANSMISSION_AUTOMATIC, 5, "312 km/charge",
     "An all-electric SUV offering a silent, eco-friendly, and economical ride."),
    ("Honda", "City", "VX 2023", 2000, Car.FUEL_PETROL, Car.TRANSMISSION_AUTOMATIC, 5, "17 km/l",
     "A refined sedan known for its comfort, smooth handling, and reliability."),
    ("Maruti Suzuki", "Ertiga", "ZXi 2023", 1900, Car.FUEL_CNG, Car.TRANSMISSION_MANUAL, 7, "26 km/kg",
     "A practical and economical 7-seater MPV, great for family outings."),
]

FAQ_DATA = [
    ("Do I need a driving license to rent a car?",
     "Yes, a valid driving license is mandatory. You will need to upload a clear photo of your license during the booking process."),
    ("Is there a security deposit?",
     "Security deposit requirements vary by car category and will be communicated by our team when your booking is confirmed."),
    ("Can I extend my booking after pickup?",
     "Yes, you can contact us directly via phone or WhatsApp to extend your rental period, subject to vehicle availability."),
    ("What documents do I need at the time of pickup?",
     "Please carry your original driving license and a valid government ID proof at the time of vehicle pickup."),
    ("How do I cancel my booking?",
     "You can cancel any booking that is still in 'Pending' status from the My Bookings page using your registered phone number."),
    ("Is fuel included in the rental price?",
     "No, fuel is not included. The car is provided with a certain fuel level and should be returned with the same level."),
    ("What happens if I return the car late?",
     "Returning the car later than the agreed time may incur additional charges calculated on a per-day basis."),
    ("Do you offer outstation trips?",
     "Yes, outstation trips are allowed on most of our vehicles. Please mention your travel plan while booking or contact our support team."),
]

TESTIMONIAL_DATA = [
    ("Ravi Kumar", 5, "Smooth booking process and the car was in excellent condition. Highly recommend Trio Self Drive!"),
    ("Priya Sharma", 5, "Affordable prices and great customer support. Will definitely book again for my next trip."),
    ("Arjun Reddy", 4, "Easy to book online and the staff was very helpful during pickup and drop."),
    ("Sneha Patel", 5, "Loved the variety of cars available. The SUV we rented was perfect for our family trip."),
    ("Kiran Rao", 4, "Quick approval and transparent pricing. No hidden charges at all."),
    ("Anjali Verma", 5, "Best self drive rental service in the city. The car was spotless and well maintained."),
]


def generate_placeholder_image(text, width=900, height=600):
    """Generate a simple branded placeholder image for a car using Pillow."""
    colors = [
        (11, 94, 215), (10, 61, 145), (37, 99, 235), (30, 64, 175), (59, 130, 246),
    ]
    bg_color = random.choice(colors)
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a simple road-stripe pattern signature at the bottom
    stripe_y = height - 60
    for x in range(0, width, 60):
        draw.rectangle([x, stripe_y, x + 30, stripe_y + 8], fill=(255, 255, 255))

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((width - text_w) / 2, (height - text_h) / 2 - 30), text, fill=(255, 255, 255), font=font)

    subtitle = "Trio Self Drive"
    bbox2 = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_w = bbox2[2] - bbox2[0]
    draw.text(((width - sub_w) / 2, (height - text_h) / 2 + 40), subtitle, fill=(220, 230, 250), font=small_font)

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return buffer


class Command(BaseCommand):
    help = "Seed the database with sample cars, FAQs, testimonials, and a default admin user."

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing cars, FAQs, and testimonials before seeding.',
        )

    def handle(self, *args, **options):
        if options['flush']:
            Car.objects.all().delete()
            FAQ.objects.all().delete()
            Testimonial.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing cars, FAQs, and testimonials deleted.'))

        # Create default admin user for dashboard access
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', email='admin@trioselfdrive.com', password='TrioAdmin@123'
            )
            self.stdout.write(self.style.SUCCESS(
                'Superuser created -> username: admin | password: TrioAdmin@123'
            ))
        else:
            self.stdout.write('Superuser "admin" already exists, skipping.')

        # Seed cars
        created_count = 0
        for brand, name, model, price, fuel, trans, seats, mileage, description in CAR_DATA:
            if Car.objects.filter(brand=brand, car_name=name, model=model).exists():
                continue
            car = Car(
                brand=brand, car_name=name, model=model, price_per_day=price,
                fuel_type=fuel, transmission=trans, seats=seats, mileage=mileage,
                description=description, is_available=True,
            )
            image_buffer = generate_placeholder_image(f"{brand}\n{name}".replace("\n", " "))
            car.image.save(f"{brand}_{name}.jpg".replace(" ", "_"), ContentFile(image_buffer.read()), save=False)
            car.save()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} cars added.'))

        # Seed FAQs
        faq_created = 0
        for order, (question, answer) in enumerate(FAQ_DATA):
            if FAQ.objects.filter(question=question).exists():
                continue
            FAQ.objects.create(question=question, answer=answer, order=order, is_active=True)
            faq_created += 1
        self.stdout.write(self.style.SUCCESS(f'{faq_created} FAQs added.'))

        # Seed Testimonials
        testimonial_created = 0
        for name, rating, comment in TESTIMONIAL_DATA:
            if Testimonial.objects.filter(customer_name=name, comment=comment).exists():
                continue
            Testimonial.objects.create(customer_name=name, rating=rating, comment=comment, is_active=True)
            testimonial_created += 1
        self.stdout.write(self.style.SUCCESS(f'{testimonial_created} testimonials added.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
