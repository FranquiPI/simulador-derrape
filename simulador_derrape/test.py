"""Pruebas rápidas. Ejecutar desde la carpeta padre: python -m simulador_derrape.test."""
from simulador_derrape import Neumatico, Vehiculo

# Presets
assert Neumatico.desde_preset("Blando").mu == 1.7
try:
    Neumatico.desde_preset("slick")
    raise AssertionError("debió fallar")
except ValueError:
    pass

# Downforce: Cd=0 -> sin carga aerodinámica; carga vertical = peso
calle = Vehiculo.auto_calle()
assert calle.downforce(80) == 0.0
assert calle.carga_vertical(80) == calle.peso

# F1 a 250 km/h (69.44 m/s): downforce ≈ 2.5 veces el peso
f1 = Vehiculo.monoplaza_f1()
v = 250 / 3.6
ratio = f1.downforce(v) / f1.peso
assert 2.0 < ratio < 3.0, ratio

# Fricción máxima crece con v² por la downforce
assert f1.friccion_maxima_plano(70) > f1.friccion_maxima_plano(30)

# Validaciones
for args in [("x", -1, 0), ("x", 100, -1)]:
    try:
        Vehiculo(args[0], args[1], args[2], Neumatico(1.0, "t"))
        raise AssertionError("debió fallar")
    except ValueError:
        pass

print(f1)
print(f"Downforce/peso a 250 km/h: {ratio:.2f}")
print("OK: todas las pruebas pasaron")