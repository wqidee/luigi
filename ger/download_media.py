#!/usr/bin/env python3
"""
Script para baixar todos os arquivos de mídia referenciados no main.1cbf12b5.js
"""
import re
import os
import requests
from urllib.parse import urljoin
from pathlib import Path

# Configurações
BASE_URL = "https://exklusive-angebote.site/ger/"
JS_FILE = "static/js/main.1cbf12b5.js"
OUTPUT_DIR = "static/media"
TIMEOUT = 30

def extract_media_files(js_content):
    """
    Extrai todas as referências a arquivos em static/media/ do conteúdo JavaScript
    """
    media_files = set()
    
    # Padrão mais abrangente: encontra qualquer referência a static/media/
    # Procura por: static/media/ seguido de caracteres válidos para nome de arquivo
    pattern = r'static/media/[a-zA-Z0-9._-]+\.(jpeg|jpg|png|gif|webp|svg|ico|mp4|mp3|webm|ogg|bmp|tiff)'
    
    matches = re.finditer(pattern, js_content, re.IGNORECASE)
    
    for match in matches:
        file_path = match.group(0)
        
        # Remove parâmetros de query e fragmentos se houver
        file_path = file_path.split('?')[0]
        file_path = file_path.split('#')[0]
        
        # Garante que começa com static/media/
        if file_path.startswith('static/media/'):
            media_files.add(file_path)
    
    # Também procura por padrões com aspas ou barras
    quote_patterns = [
        r'["\']static/media/[^"\']+\.(jpeg|jpg|png|gif|webp|svg|ico|mp4|mp3|webm|ogg|bmp|tiff)',
        r'["\']/static/media/[^"\']+\.(jpeg|jpg|png|gif|webp|svg|ico|mp4|mp3|webm|ogg|bmp|tiff)',
    ]
    
    for pattern in quote_patterns:
        matches = re.finditer(pattern, js_content, re.IGNORECASE)
        for match in matches:
            file_path = match.group(0).strip('"\'')
            
            # Remove barra inicial se houver
            if file_path.startswith('/static/media/'):
                file_path = file_path[1:]
            
            # Remove parâmetros
            file_path = file_path.split('?')[0]
            file_path = file_path.split('#')[0]
            
            if file_path.startswith('static/media/'):
                media_files.add(file_path)
    
    return sorted(media_files)

def download_file(url, output_path):
    """
    Baixa um arquivo da URL e salva no caminho especificado
    """
    try:
        print(f"Baixando: {url}")
        response = requests.get(url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva o arquivo e conta os bytes
        total_size = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)
        
        print(f"✓ Salvo: {output_path} ({total_size} bytes)")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro ao baixar {url}: {e}")
        return False

def main():
    print("=" * 60)
    print("Download de arquivos de mídia")
    print("=" * 60)
    
    # Lê o arquivo JavaScript
    if not os.path.exists(JS_FILE):
        print(f"Erro: Arquivo {JS_FILE} não encontrado!")
        return
    
    print(f"\nLendo arquivo: {JS_FILE}")
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Extrai referências a arquivos de mídia
    print("\nExtraindo referências a arquivos de mídia...")
    media_files = extract_media_files(js_content)
    
    if not media_files:
        print("Nenhum arquivo de mídia encontrado!")
        return
    
    print(f"\nEncontrados {len(media_files)} arquivo(s) de mídia:")
    for file_path in media_files:
        print(f"  - {file_path}")
    
    # Baixa os arquivos
    print(f"\nIniciando download...")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for file_path in media_files:
        # Constrói a URL completa
        full_url = urljoin(BASE_URL, file_path)
        
        # Caminho de saída local
        output_path = file_path
        
        if download_file(full_url, output_path):
            success_count += 1
        else:
            fail_count += 1
    
    # Resumo
    print("-" * 60)
    print(f"\nResumo:")
    print(f"  ✓ Sucesso: {success_count}")
    print(f"  ✗ Falhas: {fail_count}")
    print(f"  Total: {len(media_files)}")

if __name__ == "__main__":
    main()
