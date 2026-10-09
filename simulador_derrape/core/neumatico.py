class Neumatico:
    def __init__(self, mu: float, nombre: str):
        if mu <= 0:
            raise ValueError("El coeficiente de fricción del compuesto debe ser mayor a cero")
        self.mu = float(mu)
        self.nombre = nombre

    def friccion_maxima(self, fuerza_normal: float):
        """Fuerza máxima de fricción estática: F = μ · N."""
        return self.mu * fuerza_normal

    @classmethod
    def desde_preset(cls, tipo: str):
        tipo = tipo.lower()
        opciones = {
            "blando": Blando(),
            "medio": Medio(),
            "duro": Duro(),
        }
        if tipo not in opciones:
            opciones_validas = ", ".join(opciones.keys())
            raise ValueError(f"Tipo de neumático inválido: {tipo}. Opciones válidas: {opciones_validas}")
        return opciones[tipo]

    def __repr__(self):
        return f"{self.nombre} (μ={self.mu})"


class Blando(Neumatico):
    def __init__(self):
        super().__init__(1.7, "Blando")


class Medio(Neumatico):
    def __init__(self):
        super().__init__(0.8, "Medio")


class Duro(Neumatico):
    def __init__(self):
        super().__init__(1.4, "Duro")
