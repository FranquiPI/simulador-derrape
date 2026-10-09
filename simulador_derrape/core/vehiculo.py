"""Modelo del vehículo (monoplaza o auto de calle) para el simulador de derrape."""

try:
    from .neumatico import Neumatico
except ImportError:
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from simulador_derrape.core.neumatico import Neumatico

G = 9.81  # aceleración de la gravedad [m/s²]


class Vehiculo:
    """Vehículo con masa, carga aerodinámica y neumáticos."""

    def __init__(self, nombre: str, masa: float, Cd: float, neumatico: Neumatico, v: float = 0.0):
        if masa <= 0:
            raise ValueError("La masa debe ser positiva.")
        if Cd < 0:
            raise ValueError("Cd no puede ser negativo.")

        self.nombre = nombre
        self.masa = float(masa)
        self.Cd = float(Cd)
        self.neumatico = neumatico
        self.v = float(v)

    @classmethod
    def auto_calle(cls, tipo_neumatico: str = "duro") -> "Vehiculo":
        return cls(
            "Auto de calle",
            masa=1200.0,
            Cd=0.0,
            neumatico=Neumatico.desde_preset(tipo_neumatico),
            v=0.0,
        )

    @classmethod
    def monoplaza_f1(cls, tipo_neumatico: str = "blando") -> "Vehiculo":
        return cls(
            "Monoplaza F1",
            masa=800.0,
            Cd=4.0,
            neumatico=Neumatico.desde_preset(tipo_neumatico),
            v=0.0,
        )

    @property
    def peso(self):
        return self.masa * G

    def downforce(self, v):
        return self.Cd * v ** 2

    def carga_vertical(self, v):
        return self.peso + self.downforce(v)

    def friccion_maxima_plano(self, v):
        return self.neumatico.friccion_maxima(self.carga_vertical(v))

    def __repr__(self):
        return (f"Vehiculo {self.nombre}, masa = {self.masa}kg,"
                f" Cd={self.Cd}, {self.neumatico}")
        
