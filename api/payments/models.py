class Transaction(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    
    provider = models.CharField(max_length=50, db_index=True)  # MPESA / CARD
    reference = models.CharField(max_length=255, db_index=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Escrow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField("projects.Project", on_delete=models.CASCADE)
    
    amount_held = models.DecimalField(max_digits=10, decimal_places=2)
    is_released = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)