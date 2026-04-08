"""
Programa para calcular curva de calibración de Reactivo Folin-Ciocalteu
Método: Determinación de Polifenoles Totales (Método Folin-Ciocalteu)
Sustancia de referencia: Ácido gálico
Reactivo alcalino: Carbonato de sodio (Na2CO3)
"""

import sys
from tabulate import tabulate


class CalculadoraFolinCiocalteu:
    """
    Clase para calcular los volúmenes necesarios en una curva de calibración
    de Folin-Ciocalteu usando ácido gálico como estándar de referencia.
    """
    
    def __init__(self):
        self.num_puntos = 6
        self.volumen_total = 10  # mL (volumen final de cada punto)
        
    def obtener_concentraciones(self):
        """
        Obtiene del usuario las concentraciones de las soluciones madre.
        """
        print("\n" + "="*70)
        print("CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU")
        print("="*70)
        
        while True:
            try:
                entrada = input("\nConcentración de solución madre de Ácido Gálico (mg/mL): ").strip()
                if not entrada:
                    print("❌ Ingrese un valor")
                    continue
                conc_ac_galico = float(entrada)
                if conc_ac_galico <= 0:
                    print("❌ La concentración debe ser mayor a 0")
                    continue
                break
            except ValueError:
                print("❌ Ingrese un número válido")
        
        while True:
            try:
                entrada = input("Concentración de solución madre de Na2CO3 (% p/v o M): ").strip()
                if not entrada:
                    print("❌ Ingrese un valor")
                    continue
                conc_na2co3 = float(entrada)
                if conc_na2co3 <= 0:
                    print("❌ La concentración debe ser mayor a 0")
                    continue
                break
            except ValueError:
                print("❌ Ingrese un número válido")
        
        return conc_ac_galico, conc_na2co3
    
    def calcular_concentraciones_puntos(self, conc_ac_galico):
        """
        Calcula las concentraciones finales para cada punto de la curva.
        Utiliza una progresión aritmética para distribuir los puntos uniformemente.
        """
        # Rango típico: 0 a 100 mg/L (0 a 0.1 mg/mL)
        conc_minima = 0  # Blanco (concentración 0)
        conc_maxima = 100  # mg/L = 0.1 mg/mL
        
        # Crear 6 puntos distribuidos uniformemente
        concentraciones = [
            conc_minima + (conc_maxima - conc_minima) * i / (self.num_puntos - 1)
            for i in range(self.num_puntos)
        ]
        
        return concentraciones
    
    def calcular_volumenes(self, concentraciones, conc_ac_galico):
        """
        Calcula los volúmenes de solución madre de ácido gálico necesarios
        para preparar cada punto de la curva.
        
        Usa la fórmula: C1 × V1 = C2 × V2
        Donde:
        - C1 = Concentración de la solución madre (mg/mL)
        - V1 = Volumen de la solución madre (mL)
        - C2 = Concentración deseada (mg/L) = (mg/L)/1000 = mg/mL
        - V2 = Volumen final (mL) = 10 mL
        """
        volumenes = []
        
        for conc in concentraciones:
            # Convertir concentración de mg/L a mg/mL (dividir entre 1000)
            conc_mgml = conc / 1000
            
            # Calcular volumen usando C1V1 = C2V2
            if conc == 0:
                volumen = 0
            else:
                volumen = (conc_mgml * self.volumen_total) / conc_ac_galico
            
            volumenes.append(volumen)
        
        return volumenes
    
    def generar_tabla_resultados(self, concentraciones, volumenes, conc_ac_galico):
        """
        Genera una tabla con los resultados de los cálculos.
        """
        datos = []
        
        for i, (conc, vol) in enumerate(zip(concentraciones, volumenes), 1):
            datos.append([
                i,
                f"{conc:.2f}",
                f"{vol:.4f}",
                f"{self.volumen_total - vol:.4f}",
                self.volumen_total
            ])
        
        encabezados = [
            "Punto",
            "Conc. Final\n(mg/L)",
            "Vol. Ác. Gálico\n(mL)",
            "Vol. Agua\n(mL)",
            "Vol. Total\n(mL)"
        ]
        
        print("\n" + "="*70)
        print("TABLA DE VOLÚMENES PARA CURVA DE CALIBRACIÓN")
        print("="*70)
        print(tabulate(datos, headers=encabezados, tablefmt="grid"))
        
        print(f"\n📊 Solución madre Ácido Gálico: {conc_ac_galico} mg/mL")
        print(f"📏 Volumen final por punto: {self.volumen_total} mL")
    
    def generar_protocolo(self, concentraciones, volumenes, conc_ac_galico, conc_na2co3):
        """
        Genera un protocolo detallado de preparación.
        """
        print("\n" + "="*70)
        print("PROTOCOLO DE PREPARACIÓN")
        print("="*70)
        
        print(f"""
1. MATERIALES NECESARIOS:
   • Solución madre de Ácido Gálico: {conc_ac_galico} mg/mL
   • Solución madre de Na2CO3: {conc_na2co3}
   • Agua destilada/desionizada
   • Tubos de ensayo o celdas de reacción
   • Pipetas volumétricas de precisión

2. PREPARACIÓN DE PUNTOS DE LA CURVA:
""")
        
        for i, (conc, vol) in enumerate(zip(concentraciones, volumenes), 1):
            vol_agua = self.volumen_total - vol
            if vol == 0:
                print(f"""   Punto {i} (Blanco - {conc:.2f} mg/L):
      • Ácido Gálico: {vol:.4f} mL
      • Agua: {vol_agua:.4f} mL
      ✓ Este es el blanco (control negativo)
""")
            else:
                print(f"""   Punto {i} ({conc:.2f} mg/L):
      • Ácido Gálico: {vol:.4f} mL
      • Agua: {vol_agua:.4f} mL
""")
        
        print(f"""
3. PROCEDIMIENTO DE REACCIÓN:
   a) Agregar a cada punto:
      • 1 mL de Reactivo Folin-Ciocalteu (diluido 1:10 si es necesario)
      • Incubar 5 minutos a temperatura ambiente
   
   b) Agregar:
      • 1 mL de Na2CO3 ({conc_na2co3})
      • Incubar 30-60 minutos en oscuridad a temperatura ambiente
   
   c) Medir absorbancia:
      • Longitud de onda: 765 nm
      • Usar el Punto 1 (blanco) como referencia
      • Registrar lecturas en espectrofotómetro

4. CÁLCULO DE RESULTADOS:
   • Construir gráfica: Absorbancia (Y) vs Concentración (X)
   • Determinar ecuación de la recta de calibración
   • Calcular R² para validar linealidad (R² > 0.99 es aceptable)
""")
    
    def ejecutar(self):
        """
        Ejecuta el programa completo.
        """
        try:
            # Obtener concentraciones del usuario
            conc_ac_galico, conc_na2co3 = self.obtener_concentraciones()
            
            # Calcular concentraciones de los puntos
            concentraciones = self.calcular_concentraciones_puntos(conc_ac_galico)
            
            # Calcular volúmenes necesarios
            volumenes = self.calcular_volumenes(concentraciones, conc_ac_galico)
            
            # Generar tabla de resultados
            self.generar_tabla_resultados(concentraciones, volumenes, conc_ac_galico)
            
            # Generar protocolo detallado
            self.generar_protocolo(concentraciones, volumenes, conc_ac_galico, conc_na2co3)
            
            # Guardar resultados en archivo
            self.guardar_resultados(concentraciones, volumenes, conc_ac_galico, conc_na2co3)
            
        except KeyboardInterrupt:
            print("\n\n❌ Programa interrumpido por el usuario")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    
    def guardar_resultados(self, concentraciones, volumenes, conc_ac_galico, conc_na2co3):
        """
        Guarda los resultados en un archivo de texto.
        """
        nombre_archivo = "curva_calibracion_folin_ciocalteu.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU\n")
            f.write("Método de Determinación de Polifenoles Totales\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"PARÁMETROS:\n")
            f.write(f"  • Concentración Ácido Gálico (solución madre): {conc_ac_galico} mg/mL\n")
            f.write(f"  • Concentración Na2CO3 (solución madre): {conc_na2co3}\n")
            f.write(f"  • Número de puntos: {self.num_puntos}\n")
            f.write(f"  • Volumen final por punto: {self.volumen_total} mL\n\n")
            
            f.write("TABLA DE VOLÚMENES:\n")
            f.write("-"*70 + "\n")
            f.write(f"{'Punto':<8} {'Conc. (mg/L)':<15} {'Ác. Gálico (mL)':<20} {'Agua (mL)':<20}\n")
            f.write("-"*70 + "\n")
            
            for i, (conc, vol) in enumerate(zip(concentraciones, volumenes), 1):
                vol_agua = self.volumen_total - vol
                f.write(f"{i:<8} {conc:<15.2f} {vol:<20.4f} {vol_agua:<20.4f}\n")
            
            f.write("-"*70 + "\n")
        
        print(f"\n✅ Resultados guardados en: {nombre_archivo}")


def main():
    """
    Función principal del programa.
    """
    calculadora = CalculadoraFolinCiocalteu()
    calculadora.ejecutar()


if __name__ == "__main__":
    main()
