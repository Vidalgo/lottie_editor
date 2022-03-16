from typing import Dict, Any


_sentinel = object()


def assertNestedDictEqual(d1: Dict, d2: Dict, path: str = 'root'):
    if not isinstance(d1, dict):
        raise AssertionError(f'First argument is not a dictionary. path = {path}')
    if not isinstance(d2, dict):
        raise AssertionError(f'Second argument is not a dictionary. path = {path}')
    if d1.keys() != d2.keys():
        only_in_d1 = d1.keys() - d2.keys()
        only_in_d2 = d2.keys() - d1.keys()
        raise AssertionError(f'Keys do not match. path = {path}, only_in_d1 = {only_in_d1}, only_in_d2 = {only_in_d2}')
    for k, v1 in d1.items():
        assertValuesEqual(v1=v1, v2=d2[k], path=f"{path}['{k}']")


def assertValuesEqual(v1: Any, v2: Any, path):
    if isinstance(v1, dict):
        assertNestedDictEqual(v1, v2, path=path)
    if isinstance(v1, list):
        assertNestedListEqual(v1, v2, path=path)
    if v1 != v2:
        raise AssertionError(f'Values not equal. path = {path}, v1 = {v1}, v2 = {v2}')


def assertNestedListEqual(l1, l2, path):
    if not isinstance(l1, list):
        raise AssertionError(f'First argument is not a list. path = {path}')
    if not isinstance(l2, list):
        raise AssertionError(f'Second argument is not a list. path = {path}')
    if len(l1) != len(l2):
        raise AssertionError(f'Lists are not the same length. path = {path}, l1 = {l1}, l2 = {l2}')
    for i, (e1, e2) in enumerate(zip(l1, l2)):
        assertValuesEqual(e1, e2, f'{path}[{i}]')


def sort_nested_dict(d: Dict) -> Dict:
    if isinstance(d, dict):
        sd = {k: v for k, v in sorted(d.items(), key=lambda p: p[0])}
        for k, v in sd.items():
            if isinstance(v, dict):
                sd[k] = sort_nested_dict(v)
            elif isinstance(v, list):
                sd[k] = [sort_nested_dict(e) for e in v]
        return sd
    else:
        return d
