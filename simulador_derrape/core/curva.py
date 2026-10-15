# modulo para calcular la velocidad maxima en una curva con peralte
# fisica:
# sumatoria de fuerzas en y: N*cos(θ) - f*sin(θ) = m*g + Cd*v²
# sumatoria de fuerzas en x: N*sin(θ) + f*cos(θ) = m*v² / R
# con f = μ * N
# despejando queda: v_max² = R*g*k / (1 - k*Cd*R/m)
# donde k = (sin(θ) + μ*cos(θ)) / (cos(θ) - μ*sin(θ))

import math

try:
    from .vehiculo import Vehiculo, G
except ImportError:
    import sys
    from pathlib import Path
    # parche por si se corre el archivo directo desde aca
    ruta = Path(__file__).resolve().parents[2]
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))
    from simulador_derrape.core.vehiculo import Vehiculo, G


class CurvaPeraltada:

    def __init__(self, radio, angulo_peralte_deg, g=G):
        if radio <= 0:
            raise ValueError("el radio tiene que ser mayor a 0")
        if not 0 <= angulo_peralte_deg < 90:
            raise ValueError("el angulo tiene que estar en [0°, 90°)")
        if g <= 0:
            raise ValueError("la gravedad tiene que ser mayor a 0")

        self.radio = float(radio)
        self.angulo_peralte_deg = float(angulo_peralte_deg)
        self.g = float(g)

    @property
    def theta(self):
        # paso el angulo de peralte a radianes
        return math.radians(self.angulo_peralte_deg)

    def _factor_k(self, mu):
        # k = (sinθ + μ·cosθ) / (cosθ − μ·sinθ). devuelve None si el denominador <= 0
        theta = self.theta
        denominador = math.cos(theta) - mu * math.sin(theta)
        if denominador <= 0:
            return None
        return (math.sin(theta) + mu * math.cos(theta)) / denominador

    def velocidad_limite(self, mu, masa, Cd=0.0):
        # devuelve la vel maxima en m/s. si no hay limite devuelve inf
        k = self._factor_k(mu)
        if k is None:
            return math.inf

        factor_aero = 1 - k * Cd * self.radio / masa
        if factor_aero <= 0:
            return math.inf

        return math.sqrt(self.radio * self.g * k / factor_aero)

    def velocidad_maxima(self, vehiculo):
        # velocidad maxima sin derrapar [m/s] para un vehiculo
        return self.velocidad_limite(
            mu=vehiculo.neumatico.mu,
            masa=vehiculo.masa,
            Cd=vehiculo.Cd,
        )

    def velocidad_maxima_kmh(self, vehiculo):
        # lo paso a km/h
        return self.velocidad_maxima(vehiculo) * 3.6

    def velocidad_ideal(self):
        # velocidad sin friccion (μ = 0): v = sqrt(R*g*tanθ)
        return math.sqrt(self.radio * self.g * math.tan(self.theta))

    def __repr__(self):
        return (f"CurvaPeraltada(radio={self.radio} m, "
                f"peralte={self.angulo_peralte_deg}°, g={self.g} m/s²)")


def _fmt(v):
    return "sin limite (inf)" if math.isinf(v) else f"{v:6.2f} m/s ({v * 3.6:6.1f} km/h)"


if __name__ == "__main__":
    radio = 100.0    # [m]
    peralte = 10.0   # [°]
    curva = CurvaPeraltada(radio, peralte)

    print("=" * 62)
    print(" prueba 1 - caso limite (Cd = 0): auto de calle")
    print("=" * 62)
    print(f" {curva}")
    print(f" velocidad ideal (μ=0): {_fmt(curva.velocidad_ideal())}")
    for tipo in ("blando", "medio", "duro"):
        auto = Vehiculo.auto_calle(tipo)
        print(f" {auto.nombre:<14} {auto.neumatico!s:<16} -> "
              f"{_fmt(curva.velocidad_maxima(auto))}")

    print()
    print("=" * 62)
    print(" prueba 2 - valores reales f1 (Cd ≠ 0, con downforce)")
    print("=" * 62)
    for tipo in ("blando", "medio", "duro"):
        f1 = Vehiculo.monoplaza_f1(tipo)
        print(f" {f1.nombre:<14} {f1.neumatico!s:<16} -> "
              f"{_fmt(curva.velocidad_maxima(f1))}")