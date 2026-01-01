import logging
from layers import Stack, TJLayer, HospitalLayer

def main():
    logging.basicConfig(level=logging.INFO)

    stack = Stack()
    
    stack.add(TJLayer())
    stack.add(HospitalLayer())
    
    m = stack.render()
    
    m.save("heat_marker_map.html")


if __name__ == "__main__":
    main()