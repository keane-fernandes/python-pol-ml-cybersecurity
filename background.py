# Check if all directories exist in the root folder
import collect
import feature
import time
import plot


def main():
    collect.main("raw", "collect")
    feature.main("collect", "feature")
    plot.main("feature", "plot")


if __name__ == "__main__":
    main()
