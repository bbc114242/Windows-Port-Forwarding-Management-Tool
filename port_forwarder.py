#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端口转发核心功能模块
"""

import socket
import threading
import time
import logging
from typing import Dict, List, Optional, Tuple

class PortForwardRule:
    """端口转发规则类"""
    
    def __init__(self, name: str, local_port: int, target_host: str, target_port: int, enabled: bool = True):
        self.name = name
        self.local_port = local_port
        self.target_host = target_host
        self.target_port = target_port
        self.enabled = enabled
        self.is_running = False
        self.server_socket = None
        self.thread = None
        self.connections = []
        
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'name': self.name,
            'local_port': self.local_port,
            'target_host': self.target_host,
            'target_port': self.target_port,
            'enabled': self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建规则"""
        return cls(
            name=data['name'],
            local_port=data['local_port'],
            target_host=data['target_host'],
            target_port=data['target_port'],
            enabled=data.get('enabled', True)
        )

class PortForwarder:
    """端口转发器"""
    
    def __init__(self):
        self.rules: Dict[str, PortForwardRule] = {}
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('PortForwarder')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def add_rule(self, rule: PortForwardRule) -> bool:
        """添加转发规则"""
        try:
            if rule.name in self.rules:
                self.logger.warning(f"规则 {rule.name} 已存在")
                return False
                
            # 检查端口是否已被使用
            if self._is_port_in_use(rule.local_port):
                self.logger.error(f"端口 {rule.local_port} 已被使用")
                return False
                
            self.rules[rule.name] = rule
            self.logger.info(f"添加规则: {rule.name}")
            
            # 如果规则启用，立即启动
            if rule.enabled:
                return self.start_rule(rule.name)
                
            return True
            
        except Exception as e:
            self.logger.error(f"添加规则失败: {str(e)}")
            return False
    
    def remove_rule(self, rule_name: str) -> bool:
        """删除转发规则"""
        try:
            if rule_name not in self.rules:
                self.logger.warning(f"规则 {rule_name} 不存在")
                return False
                
            # 先停止规则
            self.stop_rule(rule_name)
            
            # 删除规则
            del self.rules[rule_name]
            self.logger.info(f"删除规则: {rule_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"删除规则失败: {str(e)}")
            return False
    
    def start_rule(self, rule_name: str) -> bool:
        """启动转发规则"""
        try:
            if rule_name not in self.rules:
                self.logger.error(f"规则 {rule_name} 不存在")
                return False
                
            rule = self.rules[rule_name]
            
            if rule.is_running:
                self.logger.warning(f"规则 {rule_name} 已在运行")
                return True
                
            # 创建服务器套接字
            rule.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rule.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            rule.server_socket.bind(('0.0.0.0', rule.local_port))
            rule.server_socket.listen(5)
            
            # 启动监听线程
            rule.thread = threading.Thread(target=self._listen_thread, args=(rule,))
            rule.thread.daemon = True
            rule.thread.start()
            
            rule.is_running = True
            rule.enabled = True
            
            self.logger.info(f"启动规则: {rule_name} (本地端口: {rule.local_port} -> {rule.target_host}:{rule.target_port})")
            return True
            
        except Exception as e:
            self.logger.error(f"启动规则失败: {str(e)}")
            return False
    
    def stop_rule(self, rule_name: str) -> bool:
        """停止转发规则"""
        try:
            if rule_name not in self.rules:
                self.logger.error(f"规则 {rule_name} 不存在")
                return False
                
            rule = self.rules[rule_name]
            
            if not rule.is_running:
                self.logger.warning(f"规则 {rule_name} 未在运行")
                return True
                
            # 关闭服务器套接字
            if rule.server_socket:
                rule.server_socket.close()
                rule.server_socket = None
                
            # 关闭所有连接
            for conn in rule.connections[:]:
                try:
                    conn.close()
                except:
                    pass
            rule.connections.clear()
            
            rule.is_running = False
            rule.enabled = False
            
            self.logger.info(f"停止规则: {rule_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"停止规则失败: {str(e)}")
            return False
    
    def _listen_thread(self, rule: PortForwardRule):
        """监听线程"""
        try:
            while rule.is_running and rule.server_socket:
                try:
                    client_socket, addr = rule.server_socket.accept()
                    self.logger.info(f"新连接来自 {addr} -> {rule.name}")
                    
                    # 创建转发线程
                    forward_thread = threading.Thread(
                        target=self._forward_connection,
                        args=(client_socket, rule)
                    )
                    forward_thread.daemon = True
                    forward_thread.start()
                    
                except socket.error:
                    break
                    
        except Exception as e:
            self.logger.error(f"监听线程错误: {str(e)}")
    
    def _forward_connection(self, client_socket: socket.socket, rule: PortForwardRule):
        """转发连接"""
        target_socket = None
        try:
            # 连接到目标服务器
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((rule.target_host, rule.target_port))
            
            rule.connections.extend([client_socket, target_socket])
            
            # 创建双向转发线程
            t1 = threading.Thread(target=self._transfer_data, args=(client_socket, target_socket))
            t2 = threading.Thread(target=self._transfer_data, args=(target_socket, client_socket))
            
            t1.daemon = True
            t2.daemon = True
            
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()
            
        except Exception as e:
            self.logger.error(f"转发连接错误: {str(e)}")
        finally:
            # 清理连接
            for sock in [client_socket, target_socket]:
                if sock:
                    try:
                        sock.close()
                        if sock in rule.connections:
                            rule.connections.remove(sock)
                    except:
                        pass
    
    def _transfer_data(self, source: socket.socket, destination: socket.socket):
        """传输数据"""
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except:
            pass
    
    def _is_port_in_use(self, port: int) -> bool:
        """检查端口是否被使用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return False
        except socket.error:
            return True
    
    def get_rules(self) -> List[PortForwardRule]:
        """获取所有规则"""
        return list(self.rules.values())
    
    def get_rule(self, rule_name: str) -> Optional[PortForwardRule]:
        """获取指定规则"""
        return self.rules.get(rule_name)
    
    def stop_all(self):
        """停止所有规则"""
        for rule_name in list(self.rules.keys()):
            self.stop_rule(rule_name)