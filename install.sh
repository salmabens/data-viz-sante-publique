if [ ! -d "log" ]; then
    mkdir log
    echo "Created log directory"
fi

if [ ! -d "archived/raw" ]; then
    mkdir -p archived/raw
    echo "Created archived/raw directory"
fi

if [ ! -d "archived/staged" ]; then
    mkdir -p archived/staged
    echo "Created archived/staged directory"
fi

if [ ! -d "data" ]; then
    mkdir -p data
    echo "Created data directory"
fi
