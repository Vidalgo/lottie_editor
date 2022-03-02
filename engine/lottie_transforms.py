import numpy as np
import engine.lottie_parser as lp


class Lottie_transforms(lp.Lottie_parser):
    def __init__(self, lottie_filename):
        self.anchor = []
        self.position = []
        self.rotation = []
        self.scaling = []
        self.anchor_point_transformed = []
        self.position_point_transformed = []
        self.rs_matrix = []
        self.rs_k_matrix = []
        self.transformed_anchor = np.array
        self.transformed_position = np.array
        lp.Lottie_parser.__init__(self, lottie_filename)

    def find_translations_and_calc_transformations(self, lottie_obj):
        transport_layer = self.find_object_in_lottie(lottie_obj, [{"ks": ""}])
        if not transport_layer:
            transport_layer = self.find_parent_object_in_lottie(lottie_obj, [{"ty": "tr"}])
        anchor = np.array(self.find_object_in_lottie(transport_layer, [{"a": ""}, {"k": ""}]) + [0])
        position = np.array(self.find_object_in_lottie(transport_layer, [{"p": ""}, {"k": ""}]) + [0])
        scale = np.array(self.find_object_in_lottie(transport_layer, [{"s": ""}, {"k": ""}]))
        rotation = np.array([self.find_object_in_lottie(transport_layer, [{"r": ""}, {"k": ""}])])
        self.calc_transformed_positions_k(anchor[0:3], position[0:3], rotation, scale[0:3])

    def calc_rs(self, rotation, scaling):
        sx = scaling[0] / 100
        sy = scaling[1] / 100
        cos_a = np.cos(rotation[0] * np.pi / 180)
        sin_a = np.sin(rotation[0] * np.pi / 180)

        scale_matrix = np.array([[sx, 0, 0],
                                 [0, sy, 0],
                                 [0, 0, 1]])

        rotate_matrix = np.array([[cos_a, -sin_a, 0],
                                  [sin_a, cos_a, 0],
                                  [0, 0, 1]])

        self.rs_matrix.append(rotate_matrix.dot(scale_matrix))
        if not self.rs_k_matrix:
            self.rs_k_matrix.append(self.rs_matrix[0])
        else:
            self.rs_k_matrix.append(self.rs_k_matrix[-1].dot(self.rs_matrix[-1]))

    def calc_positions(self, anchor, position):
        self.anchor_point_transformed.append(self.rs_k_matrix[-1].dot(anchor))
        if not self.position_point_transformed:
            self.position_point_transformed.append(position)
        else:
            self.position_point_transformed.append(self.rs_k_matrix[-2].dot(position))

    def calc_transformed_positions_k(self, anchor, position, rotation, scaling):
        self.anchor.append(anchor)
        self.position.append(position)
        self.rotation.append(position)
        self.scaling.append(position)
        self.calc_rs(rotation, scaling)
        self.calc_positions(anchor, position)

    def calc_transformed_positions_n(self):
        sum_anchor = sum(self.anchor_point_transformed)
        sum_position = sum(self.position_point_transformed)
        self.transformed_anchor = sum_position - sum_anchor
        self.transformed_position = sum_position - sum_anchor

    def get_anchor(self, transform_layer_obj):
        if transform_layer_obj:
            anchor = np.array(transform_layer_obj["a"]["k"])
            return anchor[0:2]

    def set_anchor(self, transform_layer_obj, anchor=[0, 0, 0]):
        if transform_layer_obj:
            transform_layer_obj["a"]["k"] = list(anchor)
            return transform_layer_obj

    def get_position(self, transform_layer_obj):
        if transform_layer_obj:
            position = np.array(transform_layer_obj["p"]["k"])
            return position[0:2]

    def set_position(self, transform_layer_obj, position=[0, 0, 0]):
        if transform_layer_obj:
            transform_layer_obj["p"]["k"] = list(position)
            return transform_layer_obj

    def get_rotation(self, transform_layer_obj):
        if transform_layer_obj:
            rotation = np.array(transform_layer_obj["r"]["k"])
            return rotation

    def set_rotation(self, transform_layer_obj, rotation=0):
        if transform_layer_obj:
            transform_layer_obj["r"]["k"] = float(rotation)
            return transform_layer_obj

    def get_scaling(self, transform_layer_obj):
        if transform_layer_obj:
            scaling = np.array(transform_layer_obj["s"]["k"])
            return scaling[0:2]

    def set_scaling(self, transform_layer_obj, scaling=[100.0, 100.0]):
        if transform_layer_obj:
            transform_layer_obj["s"]["k"] = list(np.array(scaling))
            return transform_layer_obj

    def get_rs_matrix(self, rotation, scaling):
        sx = scaling[0] / 100
        sy = scaling[1] / 100
        cos_a = np.cos(rotation * np.pi / 180)
        sin_a = np.sin(rotation * np.pi / 180)

        scale_matrix = np.array([[sx, 0],
                                 [0, sy]])

        rotate_matrix = np.array([[cos_a, -sin_a],
                                  [sin_a, cos_a]])
        rs_matrix = np.array(rotate_matrix.dot(scale_matrix))
        return rs_matrix

    # This function transforms the T layer of a lottie object around a [0, 0] anchor of transform.
    # It should be upgraded ro operate with any center of transform (when the center of an object is not the [0, 0] anchor)
    def transform_layer(self, layer_id, composition='layers', delta_position=[0, 0], delta_rotation=0,
                        delta_scale=[100, 100]):
        # Iterate through parent layers to calculate position transfrom
        if delta_position == [0, 0]:
            layers_to_iterate_through = [layer_id]
        else:
            parent_ids = self.get_layer_parents_ids(layer_id, composition)
            parent_ids.reverse()
            layers_to_iterate_through = parent_ids + [layer_id]

        transport_layer = {}
        new_anchor = []
        new_pos = []
        new_rotation = 0
        new_scale = []
        rs_matrix = np.array([[1, 0], [0, 1]])
        for parent in layers_to_iterate_through:
            transport_layer = self.get_layer_transform(parent, composition)
            delta_position = np.linalg.inv(rs_matrix).dot(delta_position)
            new_pos = self.get_position(transport_layer) + delta_position
            new_rotation = self.get_rotation(transport_layer) + delta_rotation
            new_scale = self.get_scaling(transport_layer) * (np.array(delta_scale) / 100)
            rs_matrix = self.get_rs_matrix(self.get_rotation(transport_layer), self.get_scaling(transport_layer))
            new_rs_matrix = self.get_rs_matrix(new_rotation, new_scale)
            new_anchor = np.linalg.inv(new_rs_matrix).dot(rs_matrix).dot(self.get_anchor(transport_layer))

        self.set_anchor(transport_layer, new_anchor)
        self.set_position(transport_layer, new_pos)
        self.set_rotation(transport_layer, new_rotation)
        self.set_scaling(transport_layer, new_scale)

        return transport_layer

    def transform_using_top_parent_null_layer(self, layer_id, composition='layers', anchor=[],
                                              delta_position=[0, 0], delta_rotation=0, delta_scale=[0, 0]):
        parent_id = self.get_parent_id(layer_id, composition)

        if parent_id and self.get_layer_name(parent_id, composition) == "TRANSPORT_NULL_LAYER":
            null_layer_id = parent_id
        else:
            null_layer = self.create_null_layer("TRANSPORT_NULL_LAYER")
            null_layer_id = self.get_layer_obj_id(null_layer)
            self.add_layer(null_layer, composition)
            if parent_id:
                self.set_parent_id(parent_id, null_layer_id, composition)
            self.set_parent_id(null_layer_id, layer_id, composition)
        layer_transform = self.get_layer_transform(layer_id, composition)
        null_layer_transform = self.get_layer_transform(null_layer_id, composition)
        layer_position = self.get_position(layer_transform)
        rs_matrix = self.get_rs_matrix(self.get_rotation(layer_transform), self.get_scaling(layer_transform))
        if anchor:
            new_anchor = rs_matrix.dot(anchor)
        else:
            new_anchor = rs_matrix.dot(self.get_anchor(layer_transform))
        self.set_anchor(null_layer_transform, layer_position - new_anchor)
        self.set_position(null_layer_transform, self.get_position(null_layer_transform) + layer_position - new_anchor)
        self.set_rotation(null_layer_transform, self.get_rotation(null_layer_transform) + delta_rotation)
        self.set_scaling(null_layer_transform, self.get_scaling(null_layer_transform) * (np.array(delta_scale) / 100))

        self.parse()
        self.transform_layer(null_layer_id, composition, delta_position=delta_position)


# print (np.__version__)

lottie = lsr.load_json('Squares - static.json')

Rectangle_5_shape_date = layer_transform_data()
func = Rectangle_5_shape_date.find_translations_and_calc_transformations
lsr.func_on_parent_object_in_lottie(lottie, [{"nm": "Rectangles shape layer"},
                                             {"nm": "Rectangle 1"},
                                             {"nm": "Rectangle 2"},
                                             {"nm": "Rectangle 4"},
                                             {"nm": "Rectangle 5"}],
                                    [func, func, func, func, func])
Rectangle_5_shape_date.calc_transformed_positions_n()

rectangle_layer = lsr.find_parent_object_in_lottie(lottie, [{"nm": "Rectangles shape layer"}])
rectangle_layer_data = layer_transform_data()
rectangle_layer_data.find_translations_and_calc_transformations(rectangle_layer)

pos_shift = Rectangle_5_shape_date.transformed_anchor
anchor_shift = np.array(rectangle_layer_data.anchor[0]) +\
               np.transpose(np.linalg.inv(Rectangle_5_shape_date.rs_matrix[0]).dot(np.transpose(pos_shift-np.array(rectangle_layer_data.position[0]))))

print(pos_shift)
print(anchor_shift)
