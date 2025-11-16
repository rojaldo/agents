"""
Módulo 9: Despliegue en Producción
Ejemplo 1: Production Deployment Configuration - Configuración de producción
"""

import json
import os
from datetime import datetime


class ProductionConfig:
    """Configuración de producción para AutoGen"""

    def __init__(self, environment="production"):
        self.environment = environment
        self.config = self._load_config()
        self.deployment_info = {
            "timestamp": datetime.now().isoformat(),
            "environment": environment,
            "status": "configured"
        }

    def _load_config(self):
        """Cargar configuración según ambiente"""
        configs = {
            "development": {
                "ollama_url": "http://localhost:11434",
                "model": "mistral",
                "timeout": 30,
                "log_level": "DEBUG",
                "cache_enabled": False,
                "max_workers": 2
            },
            "staging": {
                "ollama_url": "http://ollama-staging:11434",
                "model": "mistral",
                "timeout": 45,
                "log_level": "INFO",
                "cache_enabled": True,
                "max_workers": 4
            },
            "production": {
                "ollama_url": "http://ollama-prod:11434",
                "model": "mistral",
                "timeout": 60,
                "log_level": "WARNING",
                "cache_enabled": True,
                "max_workers": 8,
                "health_check_interval": 30,
                "retry_attempts": 3,
                "circuit_breaker_enabled": True
            }
        }
        return configs.get(self.environment, configs["development"])

    def get_ollama_config(self):
        """Obtener configuración de Ollama"""
        return {
            "base_url": self.config["ollama_url"],
            "model": self.config["model"],
            "timeout": self.config["timeout"]
        }

    def get_logging_config(self):
        """Obtener configuración de logging"""
        return {
            "level": self.config["log_level"],
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": f"logs/autogen_{self.environment}.log"
        }

    def get_cache_config(self):
        """Obtener configuración de caché"""
        return {
            "enabled": self.config["cache_enabled"],
            "ttl": 3600,  # 1 hora
            "max_size": 10000
        }

    def get_concurrency_config(self):
        """Obtener configuración de concurrencia"""
        return {
            "max_workers": self.config["max_workers"],
            "queue_size": self.config["max_workers"] * 10
        }

    def validate_config(self):
        """Validar configuración"""
        issues = []

        if not self.config.get("ollama_url"):
            issues.append("Falta URL de Ollama")

        if self.config.get("timeout", 0) < 10:
            issues.append("Timeout muy bajo")

        if self.config.get("max_workers", 0) < 1:
            issues.append("Debe haber al menos 1 worker")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    def get_health_check_config(self):
        """Obtener configuración de health check"""
        if self.environment == "production":
            return {
                "enabled": True,
                "interval": self.config.get("health_check_interval", 30),
                "timeout": 10,
                "retries": 3
            }
        return {"enabled": False}

    def get_security_config(self):
        """Obtener configuración de seguridad"""
        return {
            "enable_ssl": self.environment == "production",
            "rate_limiting": self.environment == "production",
            "rate_limit_requests": 100,
            "rate_limit_window": 60,  # segundos
            "require_auth": self.environment == "production",
            "api_key_validation": self.environment == "production"
        }

    def print_config(self):
        """Imprimir configuración"""
        print(f"\n{'='*60}")
        print(f"CONFIGURACIÓN DE PRODUCCIÓN - {self.environment.upper()}")
        print("="*60)

        print(f"\n🔧 Configuración Ollama:")
        ollama = self.get_ollama_config()
        for key, value in ollama.items():
            print(f"   {key}: {value}")

        print(f"\n📋 Logging:")
        logging = self.get_logging_config()
        for key, value in logging.items():
            print(f"   {key}: {value}")

        print(f"\n💾 Caché:")
        cache = self.get_cache_config()
        for key, value in cache.items():
            print(f"   {key}: {value}")

        print(f"\n⚙️  Concurrencia:")
        concurrency = self.get_concurrency_config()
        for key, value in concurrency.items():
            print(f"   {key}: {value}")

        print(f"\n🔐 Seguridad:")
        security = self.get_security_config()
        for key, value in security.items():
            print(f"   {key}: {value}")

        # Validación
        print(f"\n✓ Validación:")
        validation = self.validate_config()
        if validation["valid"]:
            print("   ✅ Configuración válida")
        else:
            for issue in validation["issues"]:
                print(f"   ❌ {issue}")

        print("="*60 + "\n")


def main():
    """Demostración de Production Config"""
    print("Demostración: Production Configuration")
    print("-" * 60)

    # Configuraciones de diferentes ambientes
    environments = ["development", "staging", "production"]

    for env in environments:
        config = ProductionConfig(env)
        config.print_config()

    # Verificación de ambiente actual
    current_env = os.getenv("ENVIRONMENT", "development")
    print(f"\n📌 Ambiente actual (variable ENVIRONMENT): {current_env}")

    prod_config = ProductionConfig(current_env)
    print(f"\n✓ Configuración cargada para: {current_env}")
    print(f"  Ollama URL: {prod_config.get_ollama_config()['base_url']}")
    print(f"  Log Level: {prod_config.get_logging_config()['level']}")
    print(f"  Cache: {'Habilitado' if prod_config.get_cache_config()['enabled'] else 'Deshabilitado'}")


if __name__ == "__main__":
    main()
