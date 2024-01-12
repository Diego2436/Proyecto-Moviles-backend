from django.db import models

class FoodTruck(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

class Usuario(models.Model):
    usuario = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    verificacion = models.CharField(max_length=3, default='NO')

class Empleado(models.Model):
    numeroEmpleado = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    rol = models.CharField(max_length=10, null=True, blank=True)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)

class Pedido(models.Model):
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pedido = models.CharField(max_length=45, null=True, blank=True)
    fecha_entrega = models.CharField(max_length=45, null=True, blank=True)
    fecha_repartidor = models.CharField(max_length=45, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=400, null=True, blank=True)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen = models.CharField(max_length=50, null=True, blank=True)
    categoria = models.CharField(max_length=20, null=True, blank=True)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)

class DetallesPedido(models.Model):
    cantidad = models.IntegerField(null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
