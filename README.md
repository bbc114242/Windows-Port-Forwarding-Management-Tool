# Windows端口转发管理工具

一个基于Python和Tkinter开发的Windows端口转发管理工具，提供图形化界面来管理端口转发规则，集成Windows netsh portproxy功能。

## 📋 目录

- [功能特性](#功能特性)
- [系统要求](#系统要求)
- [安装与使用](#安装与使用)
- [项目结构](#项目结构)
- [技术架构](#技术架构)
- [配置文件](#配置文件)
- [注意事项](#注意事项)
- [故障排除](#故障排除)
- [更新日志](#更新日志)
- [许可证](#许可证)

## 🚀 功能特性

### 核心功能
- ✅ **图形化界面**: 基于Tkinter的直观用户界面
- ✅ **规则管理**: 添加、编辑、删除端口转发规则
- ✅ **Netsh集成**: 支持Windows netsh portproxy规则的导入、同步和管理
- ✅ **双向同步**: 应用规则可同步到系统netsh，实现系统级端口转发
- ✅ **批量操作**: 支持批量启用、停用、删除规则
- ✅ **实时控制**: 可以随时启用或停用转发规则
- ✅ **数据持久化**: 自动保存和加载规则配置
- ✅ **状态监控**: 实时显示规则状态和连接数
- ✅ **分页显示**: 支持大量规则的分页浏览（5/10/20/50条每页）

### 界面特性
- 🎨 **居中显示**: 主窗口和所有对话框均居中显示
- 📄 **分页导航**: 提供首页、上页、下页、末页快速导航
- 🔍 **智能输入**: IP地址自动格式化和验证
- 🖱️ **右键菜单**: 丰富的右键操作菜单
- 📊 **状态指示**: 清晰的规则状态和连接数显示

## 💻 系统要求

### 最低要求
- **操作系统**: Windows 7/8/10/11
- **Python版本**: 3.7+（如果从源码运行）
- **架构**: 64位系统
- **内存**: 至少 100MB 可用内存
- **磁盘空间**: 至少 20MB 可用空间

### 推荐配置
- **操作系统**: Windows 10/11
- **内存**: 256MB 或更多可用内存
- **权限**: 管理员权限（用于netsh操作）

## 📦 安装与使用

### 重要提示

⚠️ **管理员权限要求**：本程序需要管理员权限才能正常运行，因为需要管理Windows系统的端口转发规则。

- 程序启动时会自动检测权限并弹出UAC（用户账户控制）提示
- 请在UAC提示中选择"是"以授予管理员权限
- 如果拒绝权限提升，程序将无法正常工作

### 方式一：使用可执行文件（推荐）
1. 下载 `WinPortForwarder.exe` 文件
2. 将文件放置到任意目录
3. 以管理员身份运行程序（右键选择"以管理员身份运行"或直接双击）

### 方式二：从源码运行
1. 克隆或下载项目源码
2. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 以管理员权限运行程序：
   ```bash
   python main.py
   ```

### 基本操作

1. **添加规则**
   - 点击工具栏的"添加规则"按钮
   - 填写本地端口、目标主机、目标端口
   - 选择是否立即启用
   - 点击确定保存

2. **编辑规则**
   - 选中要编辑的规则
   - 双击或点击"编辑规则"按钮
   - 修改相关信息后保存

3. **启用/停用规则**
   - 选中规则后点击"启用"或"停用"按钮
   - 或使用右键菜单进行操作

4. **批量操作**
   - 按住Ctrl键选择多个规则
   - 使用"批量操作"菜单进行批量启用、停用或删除

5. **Netsh集成**
   - 通过"文件"菜单导入现有netsh portproxy规则
   - 使用"Netsh管理"菜单进行系统级规则同步
   - 右键点击规则可单独同步到netsh或从netsh移除

## 📁 项目结构

```
Winlucky/
├── main.py                 # 主程序入口
├── port_forwarder.py       # 端口转发核心模块
├── rule_manager.py         # 规则管理模块
├── netsh_manager.py        # Netsh命令集成模块
├── requirements.txt        # 项目依赖
├── rules.json             # 规则配置文件（自动生成）
├── build_exe.bat          # 可执行文件构建脚本
├── WinPortForwarder.spec   # PyInstaller配置文件
├── README.md              # 项目说明
└── ui/                    # 用户界面模块
    ├── __init__.py
    ├── main_window.py     # 主窗口
    └── rule_dialog.py     # 规则编辑对话框
```

## 🏗️ 技术架构

### 核心模块
- **PortForwarder**: 端口转发核心类，处理网络连接和数据转发
- **PortForwardRule**: 转发规则数据类
- **RuleManager**: 规则管理器，提供规则的增删改查功能
- **NetshManager**: Netsh命令集成，管理系统级端口转发
- **MainWindow**: 主窗口界面类
- **RuleDialog**: 规则编辑对话框类

### 依赖关系
- **Python 3.x**: 核心运行环境
- **Tkinter**: GUI框架
- **Threading**: 多线程支持
- **JSON**: 数据存储格式
- **Subprocess**: 系统命令调用

## ⚙️ 配置文件

程序会自动在当前目录生成`rules.json`文件来保存规则配置。文件格式如下：

```json
{
  "rules": [
    {
      "name": "规则名称",
      "local_port": 8080,
      "target_host": "192.168.1.100",
      "target_port": 80,
      "enabled": true,
      "protocol": "tcp"
    }
  ]
}
```

## ⚠️ 注意事项

1. **权限要求**: netsh portproxy操作需要管理员权限
2. **防火墙设置**: 确保Windows防火墙允许程序访问网络
3. **端口冲突**: 避免使用已被其他程序占用的端口
4. **网络安全**: 谨慎开放端口，避免安全风险
5. **系统兼容**: netsh portproxy功能需要Windows Vista及以上版本

## 🔧 故障排除

### 常见问题

1. **程序无法启动**
   - 确保系统为64位Windows
   - 尝试以管理员身份运行程序

2. **端口转发不生效**
   - 检查防火墙设置
   - 确保目标服务可访问
   - 验证端口未被占用

3. **权限不足**
   - 以管理员身份运行程序
   - 检查Windows防火墙设置

4. **规则配置丢失**
   - 检查程序目录下是否有`rules.json`文件
   - 避免删除配置文件

### 日志信息

程序运行时会在控制台输出详细的日志信息，包括：
- 规则启动/停止状态
- 连接建立/断开信息
- 错误和警告信息

## 📝 更新日志

### v1.2.0 (2025-01-22)
- **架构重构**: 完全基于netsh portproxy实现
- **界面优化**: 简化菜单结构，统一操作逻辑
- **功能增强**: 系统级规则管理，跨应用兼容

### v1.1.0 (2025-08-22)
- 🆕 新增netsh portproxy集成功能
- 📥 支持导入现有系统端口转发规则
- 🔄 添加规则与系统netsh的双向同步
- 🖱️ 增强右键菜单功能

### v1.0.0 (2025-08-22)
- 🎉 首次发布
- ✨ 实现端口转发核心功能
- 🎨 优化用户界面设计
- 📄 添加分页功能支持大量规则

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

# Windows Port Forwarding Management Tool

A Windows port forwarding management tool developed with Python and Tkinter, providing a graphical interface to manage port forwarding rules with integrated Windows netsh portproxy functionality.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Usage](#installation--usage)
- [Project Structure](#project-structure)
- [Technical Architecture](#technical-architecture)
- [Configuration Files](#configuration-files)
- [Important Notes](#important-notes)
- [Troubleshooting](#troubleshooting)
- [Changelog](#changelog)
- [License](#license)

## 🚀 Features

### Core Functionality
- ✅ **Graphical Interface**: Intuitive user interface based on Tkinter
- ✅ **Rule Management**: Add, edit, delete port forwarding rules
- ✅ **Netsh Integration**: Support for importing, syncing, and managing Windows netsh portproxy rules
- ✅ **Bidirectional Sync**: Application rules can sync to system netsh for system-level port forwarding
- ✅ **Batch Operations**: Support for batch enable, disable, delete operations
- ✅ **Real-time Control**: Enable or disable forwarding rules at any time
- ✅ **Data Persistence**: Automatic saving and loading of rule configurations
- ✅ **Status Monitoring**: Real-time display of rule status and connection counts
- ✅ **Pagination**: Support for paginated browsing of large rule sets (5/10/20/50 per page)

### Interface Features
- 🎨 **Centered Display**: Main window and all dialogs are centered
- 📄 **Page Navigation**: First, previous, next, last page quick navigation
- 🔍 **Smart Input**: Automatic IP address formatting and validation
- 🖱️ **Context Menu**: Rich right-click operation menu
- 📊 **Status Indicators**: Clear rule status and connection count display

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Windows 7/8/10/11
- **Python Version**: 3.7+ (if running from source)
- **Architecture**: 64-bit system
- **Memory**: At least 100MB available memory
- **Disk Space**: At least 20MB available space

### Recommended Configuration
- **Operating System**: Windows 10/11
- **Memory**: 256MB or more available memory
- **Permissions**: Administrator privileges (for netsh operations)

## 📦 Installation & Usage

### Important Notice

⚠️ **Administrator Privileges Required**: This program requires administrator privileges to function properly, as it needs to manage Windows system port forwarding rules.

- The program will automatically detect permissions and display a UAC (User Account Control) prompt on startup
- Please select "Yes" in the UAC prompt to grant administrator privileges
- If you deny the privilege elevation, the program will not work correctly

### Method 1: Using Executable File (Recommended)
1. Download the `WinPortForwarder.exe` file
2. Place the file in any directory
3. Run the program as administrator (right-click and select "Run as administrator" or double-click directly)

### Method 2: Running from Source
1. Clone or download the project source code
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program with administrator privileges:
   ```bash
   python main.py
   ```

### Basic Operations

1. **Adding Rules**
   - Click the "Add Rule" button in the toolbar
   - Fill in local port, target host, target port
   - Choose whether to enable immediately
   - Click OK to save

2. **Editing Rules**
   - Select the rule to edit
   - Double-click or click the "Edit Rule" button
   - Modify the relevant information and save

3. **Enable/Disable Rules**
   - Select a rule and click "Enable" or "Disable" button
   - Or use the right-click menu for operations

4. **Batch Operations**
   - Hold Ctrl key to select multiple rules
   - Use "Batch Operations" menu for batch enable, disable, or delete

5. **Netsh Integration**
   - Import existing netsh portproxy rules through "File" menu
   - Use "Netsh Management" menu for system-level rule synchronization
   - Right-click rules to individually sync to netsh or remove from netsh

## 📁 Project Structure

```
Winlucky/
├── main.py                 # Main program entry point
├── port_forwarder.py       # Port forwarding core module
├── rule_manager.py         # Rule management module
├── netsh_manager.py        # Netsh command integration module
├── requirements.txt        # Project dependencies
├── rules.json             # Rule configuration file (auto-generated)
├── build_exe.bat          # Executable build script
├── WinPortForwarder.spec   # PyInstaller configuration file
├── README.md              # Project documentation
└── ui/                    # User interface modules
    ├── __init__.py
    ├── main_window.py     # Main window
    └── rule_dialog.py     # Rule editing dialog
```

## 🏗️ Technical Architecture

### Core Modules
- **PortForwarder**: Core port forwarding class handling network connections and data forwarding
- **PortForwardRule**: Forwarding rule data class
- **RuleManager**: Rule manager providing CRUD operations for rules
- **NetshManager**: Netsh command integration for system-level port forwarding management
- **MainWindow**: Main window interface class
- **RuleDialog**: Rule editing dialog class

### Dependencies
- **Python 3.x**: Core runtime environment
- **Tkinter**: GUI framework
- **Threading**: Multi-threading support
- **JSON**: Data storage format
- **Subprocess**: System command invocation

## ⚙️ Configuration Files

The program automatically generates a `rules.json` file in the current directory to save rule configurations. File format:

```json
{
  "rules": [
    {
      "name": "Rule Name",
      "local_port": 8080,
      "target_host": "192.168.1.100",
      "target_port": 80,
      "enabled": true,
      "protocol": "tcp"
    }
  ]
}
```

## ⚠️ Important Notes

1. **Permission Requirements**: netsh portproxy operations require administrator privileges
2. **Firewall Settings**: Ensure Windows Firewall allows program network access
3. **Port Conflicts**: Avoid using ports already occupied by other programs
4. **Network Security**: Be cautious when opening ports to avoid security risks
5. **System Compatibility**: netsh portproxy functionality requires Windows Vista or later

## 🔧 Troubleshooting

### Common Issues

1. **Program Won't Start**
   - Ensure system is 64-bit Windows
   - Try running the program as administrator

2. **Port Forwarding Not Working**
   - Check firewall settings
   - Ensure target service is accessible
   - Verify port is not occupied

3. **Insufficient Permissions**
   - Run program as administrator
   - Check Windows Firewall settings

4. **Rule Configuration Lost**
   - Check if `rules.json` file exists in program directory
   - Avoid deleting configuration files

### Log Information

The program outputs detailed log information to the console during runtime, including:
- Rule start/stop status
- Connection establishment/disconnection information
- Error and warning messages

## 📝 Changelog

### v1.2.0 (2025-01-22)
- **Architecture Refactoring**: Completely based on netsh portproxy implementation
- **Interface Optimization**: Simplified menu structure, unified operation logic
- **Feature Enhancement**: System-level rule management, cross-application compatibility

### v1.1.0 (2025-08-22)
- 🆕 Added netsh portproxy integration functionality
- 📥 Support for importing existing system port forwarding rules
- 🔄 Added bidirectional synchronization between rules and system netsh
- 🖱️ Enhanced right-click menu functionality

### v1.0.0 (2025-08-22)
- 🎉 Initial release
- ✨ Implemented core port forwarding functionality
- 🎨 Optimized user interface design
- 📄 Added pagination support for large rule sets

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Thank you for using Windows Port Forwarding Management Tool!**
