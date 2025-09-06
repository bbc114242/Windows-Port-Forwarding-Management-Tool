#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows端口转发管理工具
主程序入口
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from datetime import datetime
import ctypes

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from port_forwarder import PortForwarder
from rule_manager import RuleManager
from ui.main_window import MainWindow

def is_admin():
    """检查是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新启动程序"""
    if is_admin():
        # 已经是管理员权限，直接运行
        return True
    else:
        # 请求管理员权限
        try:
            # 获取当前脚本的完整路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe文件
                script = sys.executable
            else:
                # 如果是Python脚本
                script = os.path.abspath(sys.argv[0])
            
            # 使用ShellExecute以管理员权限重新启动
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                script, 
                " ".join(sys.argv[1:]), 
                None, 
                1
            )
            return False  # 当前进程应该退出
        except Exception as e:
            print(f"请求管理员权限失败: {e}")
            return False

def main():
    """主函数"""
    try:
        # 检查并请求管理员权限
        if not run_as_admin():
            # 如果权限提升失败或正在重新启动，退出当前进程
            sys.exit(0)
        
        # 以管理员权限运行主程序
        # 创建主窗口
        root = tk.Tk()
        app = MainWindow(root)
        
        # 启动应用
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()