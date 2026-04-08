#!/usr/bin/env python3
"""
CALCULADOR DE CURVA DE CALIBRACIÓN - ÁCIDO GÁLICO
Input: Concentraciones en ppm (manual)
Output: Volumen de AG (µL) y Etanol (mL) para completar a 5 mL
Volúmenes fijos: Folin-Ciocalteu y Carbonato de Sodio
"""


class CurvaCalibración:
    """Clase para gestionar la curva de calibración de Ácido Gálico"""
    
    def __init__(self):
        # Parámetros fijos
        self.concentracion_ag_madre = 3.0  # mg/mL
        self.concentracion_na2co3 = 20.0  # % w/V
        self.volumen_final = 5.0  # mL
        self.num_puntos = 6
        
        # Volúmenes fijos que el usuario agregará DESPUÉS
        self.volumen_folin_fijo = None
        self.volumen_na2co3_fijo = None
        
        # Variables dinámicas
        self.concentraciones_ppm = []
        self.resultados = []
    
    def mostrar_encabezado(self):
        """Muestra el encabezado del programa"""
        print("\n" + "=" * 150)
        print(" " * 40 + "CALCULADOR DE CURVA DE CALIBRACIÓN")
        print(" " * 50 + "ÁCIDO GÁLICO")
        print("=" * 150)
        print("\n📋 PARÁMETROS FIJOS:")
        print(f"   • Concentración Ácido Gálico (solución madre): {self.concentracion_ag_madre} mg/mL")
        print(f"   • Concentración Carbonato de Sodio: {self.concentracion_na2co3}% w/V")
        print(f"   • Volumen final deseado: {self.volumen_final} mL")
        print(f"   • Número de puntos: {self.num_puntos}")
        print("=" * 150)
    
    def solicitar_volumenes_fijos(self):
        """Solicita los volúmenes fijos de Folin y Na2CO3"""
        print("\n" + "─" * 150)
        print("VOLÚMENES FIJOS A AGREGAR (después del Ác. Gálico y Etanol)")
        print("─" * 150)
        
        try:
            self.volumen_folin_fijo = float(
                input("\nVolumen fijo de Folin-Ciocalteu a agregar en cada punto (mL): ")
            )
            
            self.volumen_na2co3_fijo = float(
                input("Volumen fijo de Carbonato de Sodio 20% a agregar en cada punto (mL): ")
            )
            
            print(f"\n✓ Volúmenes fijos registrados")
            print(f"  • Folin-Ciocalteu: {self.volumen_folin_fijo} mL")
            print(f"  • Carbonato de Sodio 20%: {self.volumen_na2co3_fijo} mL")
            
            return True
        except ValueError:
            print("❌ Error: Ingresa valores numéricos válidos")
            return False
    
    def solicitar_concentraciones(self):
        """Solicita las 6 concentraciones en ppm de forma manual"""
        print("\n" + "─" * 150)
        print("INGRESO DE CONCENTRACIONES DE ÁCIDO GÁLICO")
        print("─" * 150)
        print(f"\nIngresa {self.num_puntos} concentraciones en ppm (en orden descendente):\n")
        
        self.concentraciones_ppm = []
        
        try:
            for i in range(self.num_puntos):
                conc = float(input(f"   Punto {i + 1} - Concentración (ppm): "))
                self.concentraciones_ppm.append(conc)
            
            # Verificar que esté en orden descendente
            for i in range(len(self.concentraciones_ppm) - 1):
                if self.concentraciones_ppm[i] < self.concentraciones_ppm[i + 1]:
                    print("\n⚠️  Las concentraciones no están en orden descendente")
                    reorganizar = input("   ¿Deseas que las ordene automáticamente? (s/n): ").strip().lower()
                    if reorganizar == 's':
                        self.concentraciones_ppm.sort(reverse=True)
                    break
            
            print(f"\n✓ {self.num_puntos} concentraciones ingresadas correctamente")
            return True
        except ValueError:
            print("❌ Error: Ingresa valores numéricos válidos")
            return False
    
    def calcular_volumenes(self):
        """Calcula volumen de AG (µL) y Etanol (mL) para cada punto"""
        self.resultados = []
        
        for i, concentracion_ppm in enumerate(self.concentraciones_ppm, 1):
            # Convertir ppm a mg/mL (1 ppm = 0.001 mg/mL en soluciones diluidas)
            concentracion_mg_ml = concentracion_ppm * 0.001
            
            # Volumen de Ácido Gálico necesario (mL)
            if self.concentracion_ag_madre > 0:
                volumen_ag_ml = (concentracion_mg_ml * self.volumen_final) / self.concentracion_ag_madre
            else:
                volumen_ag_ml = 0
            
            # Convertir a microlitros
            volumen_ag_ul = volumen_ag_ml * 1000
            
            # Volumen de Etanol para completar a 5 mL
            # Se resta el volumen de AG al volumen final
            volumen_etanol = self.volumen_final - volumen_ag_ml
            
            resultado = {
                'punto': i,
                'concentracion_ppm': concentracion_ppm,
                'concentracion_mg_ml': concentracion_mg_ml,
                'volumen_ag_ml': volumen_ag_ml,
                'volumen_ag_ul': volumen_ag_ul,
                'volumen_etanol': volumen_etanol
            }
            
            self.resultados.append(resultado)
    
    def mostrar_tabla_principal(self):
        """Muestra tabla principal con los cálculos"""
        print("\n" + "=" * 140)
        print("📊 TABLA DE CÁLCULOS - VOLÚMENES A AGREGAR")
        print("=" * 140)
        
        print(f"\n{'Pto':<5} {'Concentración':<18} {'Ác. Gálico':<18} {'Ác. Gálico':<18} {'Etanol':<18}")
        print(f"{'':5} {'(ppm)':<18} {'(mL)':<18} {'(µL)':<18} {'(mL)':<18}")
        print("─" * 140)
        
        for res in self.resultados:
            print(f"{res['punto']:<5} "
                  f"{res['concentracion_ppm']:<18.4f} "
                  f"{res['volumen_ag_ml']:<18.6f} "
                  f"{res['volumen_ag_ul']:<18.2f} "
                  f"{res['volumen_etanol']:<18.6f}")
        
        print("─" * 140)
        print(f"Volumen final deseado: {self.volumen_final} mL")
        print("=" * 140)
    
    def mostrar_instrucciones_preparacion(self):
        """Muestra instrucciones paso a paso para cada punto"""
        print("\n" + "=" * 150)
        print("🧪 INSTRUCCIONES DE PREPARACIÓN POR PUNTO")
        print("=" * 150)
        
        for res in self.resultados:
            print(f"\n{'┏' + '━' * 148 + '┓'}")
            print(f"┃ PUNTO {res['punto']} - CONCENTRACIÓN: {res['concentracion_ppm']:.4f} ppm".ljust(149) + "┃")
            print(f"{'┗' + '━' * 148 + '┛'}")
            
            print(f"\n  PASO 1️⃣ : PREPARAR MATRAZ AFORADO")
            print(f"     └─ Usar un matraz aforado de {int(self.volumen_final)} mL limpio y seco")
            
            print(f"\n  PASO 2️⃣ : AGREGAR ÁCIDO GÁLICO")
            print(f"     ├─ Con pipeta de precisión, tomar {res['volumen_ag_ul']:.2f} µL")
            print(f"     │  (equivalente a {res['volumen_ag_ml']:.6f} mL)")
            print(f"     ├─ Solución madre: {self.concentracion_ag_madre} mg/mL")
            print(f"     └─ Verter en el matraz aforado")
            
            print(f"\n  PASO 3️⃣ : COMPLETAR CON ETANOL")
            print(f"     ├─ Agregar {res['volumen_etanol']:.6f} mL de etanol puro")
            print(f"     ├─ Mezclar bien")
            print(f"     └─ La solución debe alcanzar exactamente {self.volumen_final} mL")
            
            print(f"\n  PASO 4️⃣ : AGREGAR CARBONATO DE SODIO 20%")
            print(f"     ├─ Agregar {self.volumen_na2co3_fijo} mL de Carbonato de Sodio 20%")
            print(f"     └─ Mezclar cuidadosamente")
            
            print(f"\n  PASO 5️⃣ : AGREGAR FOLIN-CIOCALTEU")
            print(f"     ├─ Agregar {self.volumen_folin_fijo} mL de Folin-Ciocalteu")
            print(f"     └─ Mezclar bien")
            
            print(f"\n  PASO 6️⃣ : INCUBAR")
            print(f"     ├─ Dejar reposar 2-5 minutos")
            print(f"     └─ A temperatura ambiente (~25°C)")
            
            print(f"\n  PASO 7️⃣ : MEDIR ABSORBANCIA")
            print(f"     ├─ Transferir a cubeta de UV-Vis")
            print(f"     ├─ Longitud de onda: 765 nm")
            print(f"     └─ Registrar el valor de absorbancia")
            
            print(f"\n")
        
        print("=" * 150)
    
    def mostrar_resumen_tabla(self):
        """Muestra un resumen en tabla simple"""
        print("\n" + "=" * 140)
        print("✅ RESUMEN - VOLÚMENES EXACTOS A AGREGAR EN CADA PUNTO")
        print("=" * 140)
        
        print(f"\n{'PUNTO':<8} {'ppm':<15} {'AG (µL)':<18} {'AG (mL)':<18} {'Etanol (mL)':<18}")
        print("─" * 140)
        
        for res in self.resultados:
            print(f"{res['punto']:<8} "
                  f"{res['concentracion_ppm']:<15.4f} "
                  f"{res['volumen_ag_ul']:<18.2f} "
                  f"{res['volumen_ag_ml']:<18.6f} "
                  f"{res['volumen_etanol']:<18.6f}")
        
        print("─" * 140)
        print("\n📌 VOLÚMENES FIJOS QUE AGREGARÁS DESPUÉS:")
        print(f"   • Carbonato de Sodio 20%: {self.volumen_na2co3_fijo} mL (en cada punto)")
        print(f"   • Folin-Ciocalteu: {self.volumen_folin_fijo} mL (en cada punto)")
        
        print(f"\n{'=' * 140}\n")
    
    def mostrar_checklist(self):
        """Muestra un checklist para usar en el laboratorio"""
        print("\n" + "=" * 150)
        print("📋 CHECKLIST PARA LABORATORIO")
        print("=" * 150)
        
        print("\nMATERIALES Y REACTIVOS NECESARIOS:")
        print("  ☐ 6 Matraces aforados de 5 mL")
        print("  ☐ Pipetas de precisión (para AG)")
        print("  ☐ Pipetas volumétricas (para etanol)")
        print("  ☐ Solución madre de Ácido Gálico 3 mg/mL")
        print("  ☐ Etanol puro")
        print(f"  ☐ Carbonato de Sodio 20% (cantidad: {self.volumen_na2co3_fijo * self.num_puntos:.2f} mL total)")
        print(f"  ☐ Folin-Ciocalteu (cantidad: {self.volumen_folin_fijo * self.num_puntos:.2f} mL total)")
        
        print("\nPROCEDIMIENTO GENERAL:")
        print("  1. Para cada punto, agregar Ác. Gálico (volumen calculado en µL)")
        print("  2. Completar con Etanol hasta 5 mL (volumen calculado en mL)")
        print("  3. Agregar 20% Na₂CO₃ (volumen fijo)")
        print("  4. Agregar Folin-Ciocalteu (volumen fijo)")
        print("  5. Mezclar y dejar reposar 2-5 minutos")
        print("  6. Medir absorbancia a 765 nm")
        
        print(f"\n{'=' * 150}\n")
    
    def ejecutar(self):
        """Ejecuta el flujo completo del programa"""
        self.mostrar_encabezado()
        
        # Solicitar volúmenes fijos
        if not self.solicitar_volumenes_fijos():
            return
        
        # Solicitar concentraciones
        if not self.solicitar_concentraciones():
            return
        
        # Calcular volúmenes
        self.calcular_volumenes()
        
        # Mostrar resultados
        self.mostrar_tabla_principal()
        self.mostrar_instrucciones_preparacion()
        self.mostrar_resumen_tabla()
        self.mostrar_checklist()
        
        print("✅ ¡Proceso completado!")


def main():
    """Función principal"""
    while True:
        curva = CurvaCalibración()
        curva.ejecutar()
        
        continuar = input("\n¿Deseas calcular otra curva de calibración? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n" + "=" * 150)
            print(" " * 60 + "¡Hasta luego!")
            print("=" * 150 + "\n")
            break


if __name__ == "__main__":
    main()