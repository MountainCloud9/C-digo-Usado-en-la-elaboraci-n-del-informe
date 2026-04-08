"""
CALCULADOR DE CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU
Calcula el volumen de Ácido Gálico y masa de Carbonato de Sodio para 6 puntos
"""

class CalculadorFolinCiocalteu:
    """
    Calcula volumen de AG y masa de Na₂CO₃ para curva de calibración
    """
    
    def __init__(self):
        self.volumen_final = 5  # mL
        self.concentracion_ac_galico = None
        self.concentracion_na2co3 = None
        self.puntos_calibracion = []
    
    def obtener_datos_iniciales(self):
        """
        Obtiene los datos iniciales del usuario
        """
        print("\n" + "=" * 80)
        print("CALCULADOR DE CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU")
        print("=" * 80)
        
        try:
            self.concentracion_ac_galico = float(
                input("\nConcentración de Ácido Gálico (mg/mL): ")
            )
            
            self.concentracion_na2co3 = float(
                input("Concentración de Na₂CO₃ (% w/V): ")
            )
            
            print("\n✓ Datos capturados correctamente")
            
        except ValueError:
            print("❌ Error: Ingresa valores numéricos válidos")
            return False
        
        return True
    
    def generar_concentraciones(self):
        """
        Genera 6 puntos de calibración equiespaciados
        """
        print("\n" + "=" * 80)
        print("GENERACIÓN DE 6 PUNTOS DE CALIBRACIÓN")
        print("=" * 80)
        
        print("\n¿Cómo deseas generar los puntos?")
        print("1. Automático (0 - concentración máxima)")
        print("2. Manual (ingresa cada concentración)")
        
        opcion = input("\nSelecciona opción (1 o 2): ").strip()
        
        if opcion == '1':
            try:
                conc_maxima = float(
                    input("\nIngresa la concentración máxima deseada (mg/mL): ")
                )
                
                # Generar 6 puntos equiespaciados (incluye 0)
                self.puntos_calibracion = [
                    i * (conc_maxima / 5) for i in range(6)
                ]
                
            except ValueError:
                print("❌ Error: Ingresa un valor numérico válido")
                return False
        
        elif opcion == '2':
            print("\nIngresa las 6 concentraciones de ácido gálico (mg/mL):")
            try:
                for i in range(6):
                    conc = float(input(f"Concentración punto {i+1} (mg/mL): "))
                    self.puntos_calibracion.append(conc)
            except ValueError:
                print("❌ Error: Ingresa valores numéricos válidos")
                return False
        
        else:
            print("❌ Opción no válida")
            return False
        
        return True
    
    def calcular_volumenes(self):
        """
        Calcula los volúmenes de AG y masa de Na₂CO₃ para cada punto
        """
        resultados = []
        
        for i, concentracion in enumerate(self.puntos_calibracion, 1):
            # Volumen de Ácido Gálico en mL
            volumen_ag_ml = (concentracion * self.volumen_final) / self.concentracion_ac_galico
            
            # Convertir a microlitros
            volumen_ag_ul = volumen_ag_ml * 1000
            
            # Masa de Na₂CO₃ en gramos
            masa_na2co3 = (self.concentracion_na2co3 / 100) * self.volumen_final
            
            resultado = {
                'punto': i,
                'concentracion_ag': concentracion,
                'volumen_ag_ml': volumen_ag_ml,
                'volumen_ag_ul': volumen_ag_ul,
                'masa_na2co3': masa_na2co3
            }
            
            resultados.append(resultado)
        
        return resultados
    
    def mostrar_resultados_tabla(self, resultados):
        """
        Muestra los resultados en forma de tabla
        """
        print("\n" + "=" * 100)
        print("TABLA DE PREPARACIÓN DE 6 PUNTOS DE CALIBRACIÓN")
        print("=" * 100)
        
        print(f"\n{'Punto':<8} {'[Ác. Gálico]':<18} {'Vol. Ác. Gálico':<28} {'Masa Na₂CO₃':<15}")
        print(f"{'':8} {'(mg/mL)':<18} {'(mL)':<12} {'(µL)':<12} {'(g)':<15}")
        print("-" * 100)
        
        for resultado in resultados:
            print(f"{resultado['punto']:<8} "
                  f"{resultado['concentracion_ag']:<18.4f} "
                  f"{resultado['volumen_ag_ml']:<12.4f} "
                  f"{resultado['volumen_ag_ul']:<12.1f} "
                  f"{resultado['masa_na2co3']:<15.4f}")
        
        print("-" * 100)
        print(f"Volumen final de cada solución: {self.volumen_final} mL")
        print(f"Concentración de Na₂CO₃ usada: {self.concentracion_na2co3}% w/V")
        print("=" * 100)
    
    def mostrar_resultados_detallados(self, resultados):
        """
        Muestra los resultados de forma detallada para cada punto
        """
        print("\n" + "=" * 80)
        print("PROCEDIMIENTO DETALLADO DE PREPARACIÓN")
        print("=" * 80)
        
        for resultado in resultados:
            print(f"\n{'─' * 80}")
            print(f"PUNTO {resultado['punto']} - Concentración: {resultado['concentracion_ag']:.4f} mg/mL")
            print(f"{'─' * 80}")
            
            print(f"\n  REACTIVOS A USAR:")
            print(f"  ├─ Ácido Gálico:")
            print(f"  │  ├─ Volumen: {resultado['volumen_ag_ml']:.4f} mL")
            print(f"  │  └─ Volumen: {resultado['volumen_ag_ul']:.1f} µL")
            
            print(f"\n  └─ Carbonato de Sodio (Na₂CO₃):")
            print(f"     └─ Masa a pesar: {resultado['masa_na2co3']:.4f} g ({self.concentracion_na2co3}% w/V)")
            
            print(f"\n  PROCEDIMIENTO:")
            print(f"  1. Pesar {resultado['masa_na2co3']:.4f} g de Na₂CO₃")
            print(f"  2. En un matraz de 5 mL, agregar {resultado['volumen_ag_ul']:.1f} µL de Ácido Gálico")
            print(f"  3. Agregar el Na₂CO₃ pesado")
            print(f"  4. Agregar reactivo Folin-Ciocalteu")
            print(f"  5. Completar a {self.volumen_final} mL con etanol")
            print(f"  6. Mezclar bien")
            print(f"  7. Medir absorbancia a 765 nm")
        
        print(f"\n{'=' * 80}")
    
    def exportar_resultados(self, resultados):
        """
        Exporta los resultados a un archivo de texto
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"calibracion_folin_{timestamp}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("CURVA DE CALIBRACIÓN FOLIN-CIOCALTEU\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 100 + "\n\n")
            
            f.write("PARÁMETROS:\n")
            f.write("-" * 100 + "\n")
            f.write(f"Concentración Ácido Gálico (solución madre): {self.concentracion_ac_galico} mg/mL\n")
            f.write(f"Concentración Na₂CO₃: {self.concentracion_na2co3}% w/V\n")
            f.write(f"Volumen final de cada solución: {self.volumen_final} mL\n\n")
            
            f.write("TABLA RESUMEN:\n")
            f.write("-" * 100 + "\n")
            f.write(f"{'Punto':<8} {'[Ác. Gálico]':<18} {'Vol. Ác. Gálico':<28} {'Masa Na₂CO₃':<15}\n")
            f.write(f"{'':8} {'(mg/mL)':<18} {'(mL)':<12} {'(µL)':<12} {'(g)':<15}\n")
            f.write("-" * 100 + "\n")
            
            for resultado in resultados:
                f.write(f"{resultado['punto']:<8} "
                       f"{resultado['concentracion_ag']:<18.4f} "
                       f"{resultado['volumen_ag_ml']:<12.4f} "
                       f"{resultado['volumen_ag_ul']:<12.1f} "
                       f"{resultado['masa_na2co3']:<15.4f}\n")
            
            f.write("\n" + "=" * 100 + "\n")
            f.write("PROCEDIMIENTO DETALLADO:\n")
            f.write("=" * 100 + "\n\n")
            
            for resultado in resultados:
                f.write(f"PUNTO {resultado['punto']} - [{resultado['concentracion_ag']:.4f} mg/mL]\n")
                f.write("-" * 100 + "\n")
                f.write(f"• Ácido Gálico: {resultado['volumen_ag_ml']:.4f} mL ({resultado['volumen_ag_ul']:.1f} µL)\n")
                f.write(f"• Carbonato de Sodio: {resultado['masa_na2co3']:.4f} g\n")
                f.write(f"• Volumen final: {self.volumen_final} mL\n\n")
        
        print(f"\n✓ Resultados exportados a: {nombre_archivo}")
        return nombre_archivo
    
    def ejecutar(self):
        """
        Ejecuta el programa completo
        """
        if not self.obtener_datos_iniciales():
            return
        
        if not self.generar_concentraciones():
            return
        
        resultados = self.calcular_volumenes()
        
        # Mostrar resultados
        self.mostrar_resultados_tabla(resultados)
        self.mostrar_resultados_detallados(resultados)
        
        # Preguntar si exportar
        exportar = input("\n¿Deseas exportar los resultados a un archivo? (s/n): ").strip().lower()
        if exportar == 's':
            self.exportar_resultados(resultados)
        
        print("\n✓ Proceso completado")


def main():
    """
    Función principal
    """
    calculador = CalculadorFolinCiocalteu()
    
    while True:
        calculador.ejecutar()
        
        continuar = input("\n¿Deseas generar otra curva de calibración? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
