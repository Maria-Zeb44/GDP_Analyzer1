def main():
    cfg = load_config("config.json")
    if not cfg:
        print("Cannot load config.json — aborting")
        sys.exit(1)

    # interactive display preferred; if running headless, fall back to saving
    save_dir = cfg.get("output_dir")
    try:
        run_from_config(cfg, show=True, save_dir=save_dir)
    except Exception as exc:
        print(f"Error running dashboard: {exc}")
        print("If you're running in a headless environment, set 'output_dir' in config.json to save charts as PNGs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
