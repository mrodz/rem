from layers import Stack
from layers.tj import TJLayer
import folium

def main():
    stack = Stack()
    
    stack.add(TJLayer())
    
    m = stack.render()
    
    m.save("heat_marker_map.html")
    

if __name__ == "__main__":
    main()