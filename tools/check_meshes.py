"""Check watertightness, winding and connectivity of exported ASCII STLs."""
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def inspect_mesh(path: Path) -> dict:
    raw = np.array([[float(value) for value in line.split()[1:]]
                    for line in path.read_text().splitlines() if line.lstrip().startswith("vertex ")])
    if raw.ndim != 2 or raw.shape[1] != 3 or len(raw) % 3:
        raise ValueError(f"Malformed ASCII STL: {path}")
    vertices, inverse = np.unique(raw, axis=0, return_inverse=True)
    triangles = inverse.reshape(-1, 3)
    directed = np.concatenate([triangles[:,[0,1]], triangles[:,[1,2]], triangles[:,[2,0]]])
    edges, counts = np.unique(np.sort(directed, axis=1), axis=0, return_counts=True)
    if not np.all(counts == 2):
        raise ValueError(f"Non-watertight edges: {path}")
    ordered, orient_counts = np.unique(directed, axis=0, return_counts=True)
    if len(ordered) != 2*len(edges) or not np.all(orient_counts == 1):
        raise ValueError(f"Inconsistent face winding: {path}")
    parents = np.arange(len(vertices))
    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index
    for a,b in edges:
        pa,pb = find(a),find(b)
        if pa != pb:
            parents[pb] = pa
    components = len({find(i) for i in range(len(vertices))})
    points = raw.reshape(-1,3,3)
    volume = np.sum(np.einsum("ij,ij->i", points[:,0], np.cross(points[:,1],points[:,2])))/6
    if volume <= 0:
        raise ValueError(f"Nonpositive signed volume: {path}")
    euler = len(vertices) - len(edges) + len(triangles)
    return {"file": str(path.relative_to(ROOT)), "triangles": len(triangles),
            "vertices": len(vertices), "watertight": True, "consistent_winding": True,
            "connected_components": components, "volume_mm3": float(volume),
            "euler_characteristic": euler, "bounds_mm": [vertices.min(axis=0).tolist(),vertices.max(axis=0).tolist()]}


def main():
    reports=[]
    for name, expected_genus in [("concave_cup.stl",39),("support_frame.stl",4),("socket_fit_coupon.stl",1)]:
        report=inspect_mesh(ROOT/"results"/name)
        if report["connected_components"] != 1:
            raise ValueError(f"Detached fragments in {name}")
        if report["euler_characteristic"] != 2-2*expected_genus:
            raise ValueError(f"Unexpected hole topology in {name}: {report['euler_characteristic']}")
        reports.append(report)
        print(f"PASS {name}: one connected watertight part; {expected_genus} through-holes")
    assembled = inspect_mesh(ROOT/"results/levitator_frame.stl")
    if assembled["connected_components"] != 1:
        raise ValueError("Assembly has disconnected supporting interfaces")
    reports.append(assembled)
    print("PASS assembled preview: one connected watertight mesh; cup tabs meet frame shelves")
    (ROOT/"results/mesh_validation.json").write_text(json.dumps(reports,indent=2)+"\n")


if __name__ == "__main__":
    main()
