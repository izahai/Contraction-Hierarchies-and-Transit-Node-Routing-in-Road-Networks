# Contraction Hierarchies and Transit Node Routing

## Overview

This project utilizes **Contraction Hierarchies (CH)**, a powerful graph processing algorithm proposed by Robert Geisberger in 2008. The CH algorithm is a routing planning technique based on the concept of **node contraction**, where nodes are progressively removed from a graph while adding shortcut edges to maintain shortest path distances. This results in a Contraction Hierarchy, which includes both the original graph and the added shortcuts, along with a defined order of node "importance."

## Key Concepts

### Contraction Hierarchies (CH)

- **Node Contraction**: Nodes are contracted one at a time, preserving shortest path distances.
- **Modified Bidirectional Dijkstra**: A variant of Dijkstra's algorithm that leverages node importance to reduce search space, only relaxing edges leading to important nodes in forward search and from important nodes in backward search.
- **Preprocessing**: An extensible heuristic determines node order to minimize preprocessing time.

CHs can serve as a foundation for various routing techniques, such as:
- Hub Labels
- Transit Node Routing
- Goal-Directed Routing

### Transit Node Routing

Transit Node Routing focuses on pre-computing connections between common **access nodes** (or transit nodes). This technique is based on the observation that:
- Long-distance travel typically occurs on major roads, accessed through specific entry points.
- Short trips may not utilize these nodes, as they often remain on local roads.

By calculating and storing the shortest paths between these key access nodes, we can efficiently find the shortest path for longer trips with minimal calculations.

## References

1. Robert Geisberger. **Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks**, 2008. [PDF](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=453e6c598a903e479074d3b2c17610446749a9d7)
2. E. W. Dijkstra. **A note on two problems in connexion with graphs**. *Numerische Mathematik*, 1:269–271, 1959.
3. Hannah Bast. **Route Planning in Transportation Networks**, 2015. [PDF](https://arxiv.org/pdf/1504.05140)
4. [Contraction Hierarchies: An Illustrative Guide](https://jlazarsfeld.github.io/ch.150.project/)
5. Julian Arz, Dennis Luxen, Peter Sanders. **Transit Node Routing Reconsidered**, 2013. [PDF](https://arxiv.org/pdf/1302.5611)
6. [Wikipedia: Transit Node Routing](https://en.wikipedia.org/wiki/Transit_node_routing)
7. [Wikipedia: Contraction Hierarchies](https://en.wikipedia.org/wiki/Contraction_hierarchies)
