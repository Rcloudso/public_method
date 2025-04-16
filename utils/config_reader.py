"""
配置读取工具
支持多种配置格式(YAML, INI, .env)的读取
"""
import os
import configparser
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Union, Optional
from dotenv import load_dotenv

from utils.logger import default_logger as logger


class ConfigReader:
    """配置读取类，支持多种格式的配置文件"""
    
    @staticmethod
    def load_ini(path: Union[str, Path], section: str, option: Optional[str] = None) -> Union[str, Dict[str, str]]:
        """
        读取INI格式配置文件
        
        Args:
            path: 配置文件路径
            section: 配置节
            option: 配置选项，如果为None则返回整个节的字典
            
        Returns:
            配置值或配置字典
        """
        if not Path(path).exists():
            logger.error(f"配置文件不存在: {path}")
            raise FileNotFoundError(f"配置文件不存在: {path}")
            
        try:
            conf = configparser.ConfigParser()
            conf.read(path, encoding='utf-8')
            
            if not conf.has_section(section):
                logger.error(f"配置节不存在: {section}")
                raise ValueError(f"配置节不存在: {section}")
                
            if option is None:
                # 返回该节的所有选项
                return dict(conf[section])
            else:
                if not conf.has_option(section, option):
                    logger.error(f"配置选项不存在: {section}.{option}")
                    raise ValueError(f"配置选项不存在: {section}.{option}")
                    
                return conf.get(section, option)
        except Exception as e:
            logger.error(f"读取INI配置文件失败: {e}")
            raise
    
    @staticmethod
    def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
        """
        读取YAML格式配置文件
        
        Args:
            path: 配置文件路径
            
        Returns:
            配置字典
        """
        if not Path(path).exists():
            logger.error(f"配置文件不存在: {path}")
            raise FileNotFoundError(f"配置文件不存在: {path}")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"读取YAML配置文件失败: {e}")
            raise
    
    @staticmethod
    def load_json(path: Union[str, Path]) -> Dict[str, Any]:
        """
        读取JSON格式配置文件
        
        Args:
            path: 配置文件路径
            
        Returns:
            配置字典
        """
        if not Path(path).exists():
            logger.error(f"配置文件不存在: {path}")
            raise FileNotFoundError(f"配置文件不存在: {path}")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"读取JSON配置文件失败: {e}")
            raise
    
    @staticmethod
    def load_env(dotenv_path: Optional[Union[str, Path]] = None) -> None:
        """
        加载.env文件到环境变量
        
        Args:
            dotenv_path: .env文件路径，如果为None则自动查找
        """
        try:
            load_dotenv(dotenv_path)
            logger.debug("环境变量已加载")
        except Exception as e:
            logger.error(f"加载环境变量失败: {e}")
            raise
    
    @staticmethod
    def get_env(key: str, default: Any = None) -> str:
        """
        从环境变量中获取值
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            环境变量值
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"环境变量不存在: {key}")
        return value 