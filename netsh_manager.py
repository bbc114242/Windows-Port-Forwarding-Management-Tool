#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Netsh Portproxy 管理模块
用于读取、管理Windows系统中通过netsh interface portproxy添加的规则
"""

import subprocess
import re
import logging
from typing import List, Dict, Optional, Tuple
from port_forwarder import PortForwardRule

class NetshPortproxyRule:
    """Netsh Portproxy规则类"""
    
    def __init__(self, listen_address: str, listen_port: int, connect_address: str, connect_port: int):
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.connect_address = connect_address
        self.connect_port = connect_port
        
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'listen_address': self.listen_address,
            'listen_port': self.listen_port,
            'connect_address': self.connect_address,
            'connect_port': self.connect_port
        }
    
    def to_port_forward_rule(self, name: str = None) -> PortForwardRule:
        """转换为PortForwardRule对象"""
        if name is None:
            name = f"netsh_{self.listen_port}_{self.connect_address}_{self.connect_port}"
        
        return PortForwardRule(
            name=name,
            local_port=self.listen_port,
            target_host=self.connect_address,
            target_port=self.connect_port,
            enabled=True
        )
    
    def __str__(self):
        return f"{self.listen_address}:{self.listen_port} -> {self.connect_address}:{self.connect_port}"
    
    def __eq__(self, other):
        if not isinstance(other, NetshPortproxyRule):
            return False
        return (self.listen_address == other.listen_address and 
                self.listen_port == other.listen_port and
                self.connect_address == other.connect_address and
                self.connect_port == other.connect_port)

class NetshManager:
    """Netsh Portproxy管理器"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('NetshManager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _run_netsh_command(self, command: str) -> Tuple[bool, str]:
        """执行netsh命令"""
        try:
            # 使用chcp 65001确保UTF-8编码
            full_command = f'chcp 65001 >nul && {command}'
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                self.logger.error(f"Netsh命令执行失败: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self.logger.error("Netsh命令执行超时")
            return False, "命令执行超时"
        except Exception as e:
            self.logger.error(f"执行netsh命令时发生错误: {str(e)}")
            return False, str(e)
    
    def get_all_portproxy_rules(self) -> List[NetshPortproxyRule]:
        """获取所有netsh portproxy规则"""
        try:
            success, output = self._run_netsh_command('netsh interface portproxy show all')
            
            if not success:
                self.logger.error(f"获取portproxy规则失败: {output}")
                return []
            
            rules = []
            lines = output.split('\n')
            
            # 查找规则表格开始位置
            table_started = False
            for line in lines:
                line = line.strip()
                
                # 跳过空行和标题行
                if not line or '监听' in line or 'Listen' in line or '---' in line:
                    if '监听' in line or 'Listen' in line:
                        table_started = True
                    continue
                
                if not table_started:
                    continue
                
                # 解析规则行
                # 格式通常为: 监听地址:端口 连接地址:端口
                # 或者: Listen Address:Port Connect Address:Port
                rule = self._parse_rule_line(line)
                if rule:
                    rules.append(rule)
            
            self.logger.info(f"找到 {len(rules)} 个netsh portproxy规则")
            return rules
            
        except Exception as e:
            self.logger.error(f"获取portproxy规则时发生错误: {str(e)}")
            return []
    
    def _parse_rule_line(self, line: str) -> Optional[NetshPortproxyRule]:
        """解析规则行"""
        try:
            # 移除多余空格
            line = re.sub(r'\s+', ' ', line.strip())
            
            # 尝试多种格式解析
            patterns = [
                # 格式1: 192.168.1.1:8080 192.168.1.2:80
                r'([\d\.]+):(\d+)\s+([\d\.]+):(\d+)',
                # 格式2: *:8080 192.168.1.2:80
                r'(\*|[\d\.]+):(\d+)\s+([\d\.]+):(\d+)',
                # 格式3: 带空格的格式
                r'([\d\.\*]+)\s+(\d+)\s+([\d\.]+)\s+(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    listen_addr = match.group(1)
                    listen_port = int(match.group(2))
                    connect_addr = match.group(3)
                    connect_port = int(match.group(4))
                    
                    # 将*转换为0.0.0.0
                    if listen_addr == '*':
                        listen_addr = '0.0.0.0'
                    
                    return NetshPortproxyRule(
                        listen_address=listen_addr,
                        listen_port=listen_port,
                        connect_address=connect_addr,
                        connect_port=connect_port
                    )
            
            return None
            
        except Exception as e:
            self.logger.warning(f"解析规则行失败: {line}, 错误: {str(e)}")
            return None
    
    def add_portproxy_rule(self, listen_port: int, connect_address: str, connect_port: int, listen_address: str = "*") -> bool:
        """添加netsh portproxy规则"""
        try:
            command = f'netsh interface portproxy add v4tov4 listenaddress={listen_address} listenport={listen_port} connectaddress={connect_address} connectport={connect_port}'
            
            success, output = self._run_netsh_command(command)
            
            if success:
                self.logger.info(f"成功添加netsh规则: {listen_address}:{listen_port} -> {connect_address}:{connect_port}")
                return True
            else:
                self.logger.error(f"添加netsh规则失败: {output}")
                return False
                
        except Exception as e:
            self.logger.error(f"添加netsh规则时发生错误: {str(e)}")
            return False
    
    def delete_portproxy_rule(self, listen_port: int, listen_address: str = "*") -> bool:
        """删除netsh portproxy规则"""
        try:
            command = f'netsh interface portproxy delete v4tov4 listenaddress={listen_address} listenport={listen_port}'
            
            success, output = self._run_netsh_command(command)
            
            if success:
                self.logger.info(f"成功删除netsh规则: {listen_address}:{listen_port}")
                return True
            else:
                self.logger.error(f"删除netsh规则失败: {output}")
                return False
                
        except Exception as e:
            self.logger.error(f"删除netsh规则时发生错误: {str(e)}")
            return False
    
    def clear_all_portproxy_rules(self) -> bool:
        """清除所有netsh portproxy规则"""
        try:
            command = 'netsh interface portproxy reset'
            
            success, output = self._run_netsh_command(command)
            
            if success:
                self.logger.info("成功清除所有netsh portproxy规则")
                return True
            else:
                self.logger.error(f"清除netsh规则失败: {output}")
                return False
                
        except Exception as e:
            self.logger.error(f"清除netsh规则时发生错误: {str(e)}")
            return False
    
    def sync_rule_to_netsh(self, rule: PortForwardRule) -> bool:
        """将应用规则同步到netsh"""
        try:
            # 先检查是否已存在相同规则
            existing_rules = self.get_all_portproxy_rules()
            for existing_rule in existing_rules:
                if existing_rule.listen_port == rule.local_port:
                    # 如果已存在，先删除
                    self.delete_portproxy_rule(existing_rule.listen_port, existing_rule.listen_address)
            
            # 添加新规则
            return self.add_portproxy_rule(
                listen_port=rule.local_port,
                connect_address=rule.target_host,
                connect_port=rule.target_port
            )
        except Exception as e:
            self.logger.error(f"同步规则到netsh失败: {str(e)}")
            return False
    
    def remove_rule_from_netsh(self, rule: PortForwardRule) -> bool:
        """从netsh中移除规则"""
        try:
            return self.delete_portproxy_rule(listen_port=rule.local_port)
        except Exception as e:
            self.logger.error(f"从netsh移除规则失败: {str(e)}")
            return False
    
    def is_admin_required(self) -> bool:
        """检查是否需要管理员权限"""
        try:
            # 尝试执行一个简单的netsh命令来检查权限
            success, _ = self._run_netsh_command('netsh interface portproxy show all')
            return success
        except Exception:
            return False
    
    def get_netsh_rules_as_port_forward_rules(self) -> List[PortForwardRule]:
        """获取netsh规则并转换为PortForwardRule格式"""
        netsh_rules = self.get_all_portproxy_rules()
        port_forward_rules = []
        
        for i, netsh_rule in enumerate(netsh_rules):
            name = f"netsh_imported_{i+1}_{netsh_rule.listen_port}"
            port_forward_rule = netsh_rule.to_port_forward_rule(name)
            port_forward_rules.append(port_forward_rule)
        
        return port_forward_rules