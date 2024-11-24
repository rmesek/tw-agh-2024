import re
from pathlib import Path
from itertools import product
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    import networkx as nx


class FoataAnalyzer:
    _actions: dict[str, str] = {}
    _alphabet: set[str] = set()
    _word: str = ""
    _relations: dict[str, tuple[str, set[str]]] = {}
    _dependencies: set[tuple[str, str]] = set()
    _independencies: set[tuple[str, str]] = set()
    _fnf: tuple[set[str], ...] = ()
    _graph: tuple[str, Optional["nx.DiGraph"]] = ("", None)

    def __init__(self, file_path: Path, nxgraph: bool = False):
        self._file_path = file_path
        self._nxgraph = nxgraph
        self._analyze()

    def _analyze(self) -> None:
        file_content = self._read_file()
        self._parse_input(file_content)
        self._calculate_relations()
        self._calculate_dependencies()
        self._fnf = self.calculate_foata_normal_form(self._dependencies, self._word)
        if self._nxgraph:
            self._graph = self.calculate_dependency_graph(self._fnf, nxgraph=True)
        else:
            self._graph = self.calculate_dependency_graph(self._fnf)

    def _read_file(self) -> str:
        with open(self._file_path) as file:
            return file.read()

    def _parse_input(self, input_text: str) -> None:
        actions_pattern = re.findall(r"\(([a-z])\)\s+(\w+\s*:=\s*[^\n]+)", input_text)
        if actions_pattern:
            for symbol, action in actions_pattern:
                self._actions[symbol] = action
        else:
            raise ValueError("No actions found in input text")

        alphabet_pattern = re.search(r"A = {([a-zA-Z,\s]+)}", input_text)
        if alphabet_pattern:
            for symbol in alphabet_pattern.group(1).replace(" ", "").replace(",", ""):
                self._alphabet.add(symbol)
        else:
            raise ValueError("No alphabet found in input text")

        word_pattern = re.search(r"w = ([a-zA-Z]+)", input_text)
        if word_pattern:
            self._word = word_pattern.group(1)
        else:
            raise ValueError("No word found in input text")

    def _calculate_relations(self) -> None:
        for symbol, action in self._actions.items():
            # y := y + 2z => y, {y, z}
            l_pattern = re.search(r"(\w+)\s*:=", action)
            if l_pattern:
                l_symbol = l_pattern.group(1)
            else:
                raise ValueError("No left symbol found in action")

            r_patterns = re.findall(r"([a-zA-Z])", action)
            if r_patterns:
                r_symbols = set(r_patterns)
            else:
                raise ValueError("No right symbols found in action")

            self._relations[symbol] = (l_symbol, r_symbols)

    def _calculate_dependencies(self) -> None:
        for a, b in product(self._alphabet, repeat=2):
            l_symbol_a, r_symbols_a = self._relations[a]
            l_symbol_b, r_symbols_b = self._relations[b]

            if l_symbol_a in r_symbols_b or l_symbol_b in r_symbols_a:
                self._dependencies.add((a, b))
            else:
                self._independencies.add((a, b))

    @staticmethod
    def calculate_foata_normal_form(
        dependencies: set[tuple[str, str]],
        trace: str,
    ) -> tuple[set[str], ...]:
        """
        Calculate the Foata normal form for a given trace.

        Args:
            dependencies: The set of dependencies.
            trace: The trace to calculate the Foata normal form for.

        Returns:
            The Foata normal form for the given trace as a tuple of sets.

        Example:
            >>> dependencies = {('a', 'a'), ('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'b'), ('b', 'd'),
                                ('c', 'a'), ('c', 'c'), ('c', 'd'), ('d', 'b'), ('d', 'c'), ('d', 'd')}
            >>> trace = 'baadcb'
            >>> calculate_foata_normal_form(dependencies, trace)
            ({'b'}, {'d', 'a'}, {'a'}, {'b', 'c'})
        """
        if not trace:
            return ()
        levels = [1 for _ in range(len(trace))]
        for i, symbol_i in enumerate(trace):
            for j in range(i):
                symbol_j = trace[j]
                if (symbol_j, symbol_i) in dependencies:
                    levels[i] = max(levels[i], levels[j] + 1)
        max_level = max(levels)
        blocks: list[set[str]] = [set() for _ in range(max_level)]
        for symbol, level in zip(trace, levels):
            blocks[level - 1].add(symbol)
        foata_normal_form = tuple(blocks)
        return foata_normal_form

    @staticmethod
    def calculate_dependency_graph(
        foata_normal_form: tuple[set[str], ...],
        nxgraph: bool = False,
    ) -> tuple[str, Optional["nx.DiGraph"]]:
        """
        Returns the minimal dependency graph for the given trace as graphviz dot string.

        Args:
            foata_normal_form: The Foata normal form for the given trace.
            nxgraph: Whether to return a networkx graph object.

        Returns:
            The minimal dependency graph for the given trace as a graphviz dot string.
            If nxgraph is True, a tuple of the graphviz dot string and the networkx graph object is returned.

        Example:
            >>> foata_normal_form = ({'b'}, {'d', 'a'}, {'a'}, {'b', 'c'})
            >>> graph = calculate_dependency_graph(foata_normal_form)
            >>> graph
            digraph {
            1 [label=b];
            2 [label=a];
            3 [label=d];
            4 [label=a];
            5 [label=b];
            6 [label=c];
            1 -> 2;
            1 -> 3;
            2 -> 4;
            3 -> 4;
            4 -> 5;
            4 -> 6;
            }
        """
        graph = None
        if nxgraph:
            import networkx as nx

            graph = nx.DiGraph()

        graph_dot_str = "digraph {\n"
        node_id = 1
        nodes = {}  # node_id: symbol
        node_blocks = []  # node_ids per block
        for block in foata_normal_form:
            block_node_ids = []
            for symbol in sorted(block):
                nodes[node_id] = symbol
                graph_dot_str += f"{node_id} [label={symbol}];\n"
                if graph is not None:
                    graph.add_node(node_id, label=symbol)
                block_node_ids.append(node_id)
                node_id += 1
            node_blocks.append(block_node_ids)
        # Create edges based on dependencies implied by block positions
        for i in range(len(node_blocks) - 1):
            current_block = node_blocks[i]
            next_block = node_blocks[i + 1]
            for current_node in current_block:
                for next_node in next_block:
                    graph_dot_str += f"{current_node} -> {next_node};\n"
                    if graph is not None:
                        graph.add_edge(current_node, next_node)
        graph_dot_str += "}"
        return graph_dot_str, graph

    @property
    def dependency_relation(self) -> str:
        return str(sorted(self._dependencies))

    @property
    def independence_relation(self) -> str:
        return str(sorted(self._independencies))

    @property
    def foata_normal_form(self) -> str:
        return "".join(f"({''.join(sorted(block))})" for block in self._fnf)

    @property
    def dependency_graph(self) -> str:
        return self._graph[0]

    def plot_dependency_graph(self) -> None:
        import matplotlib.pyplot as plt
        import networkx as nx

        graph = self._graph[1]
        if graph is None:
            print("Dependency graph not available")
            return
        pos = nx.shell_layout(graph)
        nx.draw(graph, pos=pos, with_labels=False)
        nx.draw_networkx_labels(
            graph,
            pos=pos,
            labels=nx.get_node_attributes(graph, "label"),
        )
        plt.show()


if __name__ == "__main__":
    pass
