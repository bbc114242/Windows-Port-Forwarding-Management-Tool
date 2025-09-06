#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则管理模块 - 基于netsh portproxy
"""

import json
import os
from typing import List, Dict, Optional
from port_forwarder import PortForwardRule, PortForwarder
from netsh_manager import NetshManager

class RuleManager:
    """规则管理器 - 直接基于netsh portproxy规则"""
    
    def __init__(self, config_file: str = "rules.json"):
        self.config_file = config_file  # 保留用于兼容性，但不再使用
        self.netsh_manager = NetshManager()
        # 不再使用内部PortForwarder，所有操作直接基于netsh
        self.load_rules_from_netsh()
    
    def add_rule(self, name: str, local_port: int, target_host: str, target_port: int, enabled: bool = True) -> bool:
        """添加规则到netsh portproxy"""
        try:
            rule = PortForwardRule(name, local_port, target_host, target_port, enabled)
            if enabled:
                # 直接添加到netsh
                success = self.netsh_manager.add_portproxy_rule(local_port, target_host, target_port)
            else:
                # 如果不启用，只是记录规则信息（可以通过注释或其他方式）
                success = True
            return success
        except Exception as e:
            print(f"添加规则失败: {str(e)}")
            return False
    
    def remove_rule(self, rule_name: str) -> bool:
        """从netsh portproxy删除规则"""
        try:
            # 根据规则名称找到对应的netsh规则
            netsh_rules = self.netsh_manager.get_all_portproxy_rules()
            target_rule = None
            
            # 通过规则名称匹配查找规则
            # 规则名称格式通常是 "Rule_端口号"
            for rule in netsh_rules:
                # 生成规则名称用于匹配
                generated_name = f"Rule_{rule.listen_port}"
                if generated_name == rule_name:
                    target_rule = rule
                    break
            
            if target_rule:
                success = self.netsh_manager.delete_portproxy_rule(target_rule.listen_port)
            else:
                # 如果找不到规则，可能已经被删除
                success = True
            return success
        except Exception as e:
            print(f"删除规则失败: {str(e)}")
            return False
    
    def update_rule(self, old_name: str, new_name: str, local_port: int, target_host: str, target_port: int, enabled: bool = True) -> bool:
        """更新netsh portproxy规则"""
        try:
            # 先删除旧规则
            old_rule = self.get_rule(old_name)
            if not old_rule:
                return False
            
            # 从netsh删除旧规则
            success = self.remove_rule(old_name)
            if not success:
                return False
            
            # 添加新规则
            success = self.add_rule(new_name, local_port, target_host, target_port, enabled)
            return success
            
        except Exception as e:
            print(f"更新规则失败: {str(e)}")
            return False
    
    def enable_rule(self, rule_name: str) -> bool:
        """启用规则（添加到netsh portproxy）"""
        try:
            # 从存储的规则信息中获取规则详情（需要实现规则信息存储）
            # 这里暂时通过netsh规则查找，实际可能需要额外的元数据存储
            netsh_rules = self.netsh_manager.get_all_portproxy_rules()
            for rule in netsh_rules:
                if hasattr(rule, 'name') and rule.name == rule_name:
                    # 规则已存在于netsh中，认为已启用
                    return True
            
            # 如果规则不在netsh中，需要从某处获取规则信息并添加
            # 这里需要额外的逻辑来存储和检索规则元数据
            print(f"规则 {rule_name} 的详细信息需要从元数据中获取")
            return False
            
        except Exception as e:
            print(f"启用规则失败: {str(e)}")
            return False
    
    def disable_rule(self, rule_name: str) -> bool:
        """停用规则（从netsh portproxy移除）"""
        try:
            # 直接调用remove_rule方法
            return self.remove_rule(rule_name)
            
        except Exception as e:
            print(f"停用规则失败: {str(e)}")
            return False
    
    def batch_enable(self, rule_names: List[str]) -> Dict[str, bool]:
        """批量启用规则"""
        results = {}
        for name in rule_names:
            results[name] = self.enable_rule(name)
        return results
    
    def batch_disable(self, rule_names: List[str]) -> Dict[str, bool]:
        """批量停用规则"""
        results = {}
        for name in rule_names:
            results[name] = self.disable_rule(name)
        return results
    
    def batch_delete(self, rule_names: List[str]) -> Dict[str, bool]:
        """批量删除规则"""
        results = {}
        for name in rule_names:
            results[name] = self.remove_rule(name)
        return results
    
    def get_all_rules(self) -> List[PortForwardRule]:
        """获取所有netsh portproxy规则"""
        try:
            netsh_rules = self.netsh_manager.get_all_portproxy_rules()
            port_forward_rules = []
            
            for rule in netsh_rules:
                # 将netsh规则转换为PortForwardRule格式
                name = getattr(rule, 'name', f"Rule_{rule.listen_port}")
                port_rule = PortForwardRule(
                    name=name,
                    local_port=rule.listen_port,
                    target_host=rule.connect_address,
                    target_port=rule.connect_port,
                    enabled=True  # netsh中的规则都是启用状态
                )
                port_forward_rules.append(port_rule)
            
            return port_forward_rules
        except Exception as e:
            print(f"获取规则失败: {str(e)}")
            return []
    
    def get_rule(self, rule_name: str) -> Optional[PortForwardRule]:
        """获取指定规则"""
        all_rules = self.get_all_rules()
        for rule in all_rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def load_rules_from_netsh(self) -> bool:
        """从netsh加载规则（替代原来的load_rules）"""
        try:
            # 直接从netsh读取，不需要额外操作
            return True
        except Exception as e:
            print(f"从netsh加载规则失败: {str(e)}")
            return False
    
    def save_rules(self) -> bool:
        """保存规则（基于netsh的实现不需要额外保存）"""
        # netsh规则自动持久化，不需要额外保存操作
        return True
    
    def load_rules(self) -> bool:
        """加载规则（已由load_rules_from_netsh替代）"""
        return self.load_rules_from_netsh()
    
    def export_rules(self, file_path: str) -> bool:
        """导出netsh规则"""
        try:
            rules_data = []
            for rule in self.get_all_rules():
                rules_data.append(rule.to_dict())
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"导出规则失败: {str(e)}")
            return False
    
    def import_rules(self, file_path: str, replace: bool = False) -> bool:
        """导入规则到netsh"""
        try:
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            
            if replace:
                # 清空现有netsh规则
                self.netsh_manager.clear_all_portproxy_rules()
            
            for rule_data in rules_data:
                rule = PortForwardRule.from_dict(rule_data)
                if rule.enabled:
                    self.netsh_manager.add_portproxy_rule(
                        rule.local_port, rule.target_host, rule.target_port
                    )
            
            return True
            
        except Exception as e:
            print(f"导入规则失败: {str(e)}")
            return False
    
    def get_rule_status(self, rule_name: str) -> Dict[str, any]:
        """获取规则状态"""
        rule = self.get_rule(rule_name)
        if not rule:
            return {}
        
        return {
            'name': rule.name,
            'local_port': rule.local_port,
            'target_host': rule.target_host,
            'target_port': rule.target_port,
            'enabled': rule.enabled,
            'is_running': rule.enabled,  # netsh中的规则都是运行状态
            'connections': 0  # netsh无法直接获取连接数
        }
    
    def get_all_status(self) -> List[Dict[str, any]]:
        """获取所有规则状态"""
        status_list = []
        for rule in self.get_all_rules():
            status_list.append(self.get_rule_status(rule.name))
        return status_list
    
    def set_netsh_sync(self, enabled: bool) -> bool:
        """设置是否同步到netsh（基于netsh的实现中此方法保留兼容性）"""
        # 基于netsh的实现中，所有操作都直接作用于netsh
        return True
    
    def sync_all_to_netsh(self) -> Dict[str, bool]:
        """同步所有规则到netsh（基于netsh的实现中规则已在netsh中）"""
        results = {}
        try:
            for rule in self.get_all_rules():
                results[rule.name] = True  # 规则已在netsh中
            return results
        except Exception as e:
            print(f"同步所有规则到netsh失败: {str(e)}")
            return {}
    
    def clear_netsh_rules(self) -> bool:
        """清除所有netsh规则"""
        try:
            return self.netsh_manager.clear_all_portproxy_rules()
        except Exception as e:
            print(f"清除netsh规则失败: {str(e)}")
            return False
    
    def get_netsh_rules(self) -> List[Dict]:
        """获取当前netsh规则"""
        try:
            netsh_rules = self.netsh_manager.get_all_portproxy_rules()
            return [rule.to_dict() for rule in netsh_rules]
        except Exception as e:
            print(f"获取netsh规则失败: {str(e)}")
            return []
    
    def cleanup(self):
        """清理资源"""
        # 基于netsh的实现不需要额外清理
        pass