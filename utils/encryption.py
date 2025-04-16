"""
加密工具模块
提供多种加密算法和安全的数据处理方法
"""
import os
import hashlib
import base64
from typing import Union, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from utils.logger import default_logger as logger


class Encryption:
    """加密工具类，提供多种加密方法"""
    
    @staticmethod
    def md5_encrypt(data: Union[str, bytes]) -> str:
        """
        计算MD5摘要（注意：不应用于密码存储，仅用于数据完整性校验）
        
        Args:
            data: 需要计算摘要的数据
            
        Returns:
            MD5摘要字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
            
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def sha256_encrypt(data: Union[str, bytes]) -> str:
        """
        计算SHA256摘要
        
        Args:
            data: 需要计算摘要的数据
            
        Returns:
            SHA256摘要字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
            
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def generate_key() -> bytes:
        """
        生成Fernet加密密钥
        
        Returns:
            加密密钥
        """
        return Fernet.generate_key()
    
    @staticmethod
    def generate_key_from_password(password: Union[str, bytes], salt: Optional[bytes] = None) -> bytes:
        """
        从密码生成加密密钥
        
        Args:
            password: 密码
            salt: 盐值，如果为None则随机生成
            
        Returns:
            (密钥, 盐值)元组
        """
        if salt is None:
            salt = os.urandom(16)
            
        if isinstance(password, str):
            password = password.encode("utf-8")
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key, salt
    
    @staticmethod
    def encrypt_data(data: Union[str, bytes], key: bytes) -> bytes:
        """
        加密数据
        
        Args:
            data: 需要加密的数据
            key: 加密密钥
            
        Returns:
            加密后的数据
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
            
        f = Fernet(key)
        return f.encrypt(data)
    
    @staticmethod
    def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
        """
        解密数据
        
        Args:
            encrypted_data: 加密后的数据
            key: 加密密钥
            
        Returns:
            解密后的数据
        """
        try:
            f = Fernet(key)
            return f.decrypt(encrypted_data)
        except Exception as e:
            logger.error(f"解密失败: {e}")
            raise 