#!/usr/bin/env python3
"""
Utilitaire de compression ZIP pour les fichiers CBZ volumineux
Compresse automatiquement les fichiers dépassant 50MB pour Telegram
"""

import os
import zipfile
import shutil
from utils.beautiful_progress import BeautifulLogger


class ZipCompressor:
    """Gestionnaire de compression ZIP pour fichiers volumineux"""
    
    TELEGRAM_MAX_SIZE = 50 * 1024 * 1024  # 50 MB en bytes
    
    @staticmethod
    def get_file_size_mb(file_path):
        """Retourne la taille du fichier en MB"""
        if not os.path.exists(file_path):
            return 0
        return os.path.getsize(file_path) / (1024 * 1024)
    
    @staticmethod
    def needs_compression(file_path):
        """Vérifie si le fichier dépasse la limite Telegram"""
        file_size = os.path.getsize(file_path)
        return file_size > ZipCompressor.TELEGRAM_MAX_SIZE
    
    @staticmethod
    def compress_file(file_path, output_dir=None, compression_level=9):
        """
        Compresse un fichier CBZ en ZIP pour respecter les limites Telegram
        
        Args:
            file_path (str): Chemin vers le fichier à compresser
            output_dir (str): Répertoire de sortie (par défaut: même répertoire)
            compression_level (int): Niveau de compression ZIP (0-9, 9=maximum)
            
        Returns:
            tuple: (zip_path, original_size_mb, compressed_size_mb, compression_ratio)
        """
        if not os.path.exists(file_path):
            BeautifulLogger.error(f"Fichier non trouvé: {file_path}")
            return None
        
        # Calculer les tailles
        original_size = os.path.getsize(file_path)
        original_size_mb = original_size / (1024 * 1024)
        
        # Définir le chemin de sortie
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        zip_path = os.path.join(output_dir, f"{base_name}_compressed.zip")
        
        BeautifulLogger.info(f"Compression en cours... ({original_size_mb:.1f} MB)", "📦")
        
        try:
            # Créer le fichier ZIP avec compression maximale
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zip_file:
                zip_file.write(file_path, os.path.basename(file_path))
            
            # Calculer la compression
            compressed_size = os.path.getsize(zip_path)
            compressed_size_mb = compressed_size / (1024 * 1024)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            BeautifulLogger.success(f"Compression réussie: {original_size_mb:.1f} MB → {compressed_size_mb:.1f} MB ({compression_ratio:.1f}% de réduction)")
            
            return zip_path, original_size_mb, compressed_size_mb, compression_ratio
            
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors de la compression: {e}")
            return None
    
    @staticmethod
    def compress_multiple_files(file_paths, zip_name, output_dir):
        """
        Compresse plusieurs fichiers CBZ dans un seul ZIP
        Utilisé pour les téléchargements multiples ou les tomes
        
        Args:
            file_paths (list): Liste des chemins des fichiers à compresser
            zip_name (str): Nom du fichier ZIP de sortie
            output_dir (str): Répertoire de sortie
            
        Returns:
            tuple: (zip_path, total_original_mb, compressed_mb, file_count)
        """
        if not file_paths:
            BeautifulLogger.error("Aucun fichier à compresser")
            return None
        
        zip_path = os.path.join(output_dir, f"{zip_name}.zip")
        total_original_size = 0
        file_count = 0
        
        BeautifulLogger.info(f"Compression de {len(file_paths)} fichiers...", "📦")
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        total_original_size += file_size
                        file_count += 1
                        
                        # Ajouter le fichier au ZIP
                        zip_file.write(file_path, os.path.basename(file_path))
                        BeautifulLogger.info(f"Ajouté: {os.path.basename(file_path)} ({file_size / (1024*1024):.1f} MB)")
            
            # Calculer les statistiques finales
            total_original_mb = total_original_size / (1024 * 1024)
            compressed_size = os.path.getsize(zip_path)
            compressed_mb = compressed_size / (1024 * 1024)
            compression_ratio = (1 - compressed_size / total_original_size) * 100
            
            BeautifulLogger.success(f"Archive créée: {file_count} fichiers, {total_original_mb:.1f} MB → {compressed_mb:.1f} MB ({compression_ratio:.1f}% de réduction)")
            
            return zip_path, total_original_mb, compressed_mb, file_count
            
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors de la compression multiple: {e}")
            return None
    
    @staticmethod
    def should_compress_for_telegram(file_path):
        """
        Détermine si un fichier doit être compressé pour Telegram
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            bool: True si compression nécessaire
        """
        if not os.path.exists(file_path):
            return False
        
        file_size = os.path.getsize(file_path)
        return file_size > ZipCompressor.TELEGRAM_MAX_SIZE
    
    @staticmethod
    def get_compression_message(original_mb, compressed_mb):
        """
        Génère un message explicatif pour l'utilisateur
        
        Args:
            original_mb (float): Taille originale en MB
            compressed_mb (float): Taille compressée en MB
            
        Returns:
            str: Message explicatif
        """
        if compressed_mb > 50:
            return (f"⚠️ **Fichier compressé en ZIP**\n"
                   f"📦 Taille originale: {original_mb:.1f} MB\n"
                   f"📦 Taille compressée: {compressed_mb:.1f} MB\n"
                   f"⚠️ **ATTENTION**: Le fichier dépasse encore 50MB même compressé!")
        else:
            reduction = ((original_mb - compressed_mb) / original_mb) * 100
            return (f"📦 **Fichier compressé en ZIP**\n"
                   f"💾 Taille originale: {original_mb:.1f} MB\n"
                   f"📦 Taille finale: {compressed_mb:.1f} MB\n"
                   f"✅ Réduction: {reduction:.1f}% (compatible Telegram)")


if __name__ == "__main__":
    # Test de compression
    test_file = "test.cbz"
    if os.path.exists(test_file):
        result = ZipCompressor.compress_file(test_file)
        if result:
            zip_path, orig_mb, comp_mb, ratio = result
            print(f"Compression: {orig_mb:.1f}MB → {comp_mb:.1f}MB ({ratio:.1f}%)")