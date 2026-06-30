from django.db import models


class ContactMessage(models.Model):
    """Stores messages submitted through the public Contact Us page."""

    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class FAQ(models.Model):
    """Frequently Asked Questions shown on the public FAQ page."""

    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    """Customer testimonials shown on the homepage."""

    customer_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating out of 5")
    comment = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.customer_name} ({self.rating}/5)"
