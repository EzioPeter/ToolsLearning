import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig  # Hydra 配置字典类型

# 装饰器参数：config_path（配置目录）、config_name（默认配置文件名）
@hydra.main(config_path="conf", config_name="default", version_base="1.3")
def main(cfg: DictConfig) -> None:
    # 访问配置（DictConfig 支持点语法）
    print("数据库配置：")
    print(f"  地址：{cfg.db.host}:{cfg.db.port}")
    print(f"  账号：{cfg.db.username}/{cfg.db.password}")
    
    print("\n服务配置：")
    print(f"  端口：{cfg.server.port}")
    print(f"  调试模式：{cfg.server.debug}")
    
    # 查看 Hydra 运行信息（如配置文件路径、命令行参数）
    print(f"\nHydra 配置路径：{HydraConfig.get().runtime.config_sources}")

if __name__ == "__main__":
    main()
