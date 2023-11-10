from typing import List

import numpy as np


class HelmertTransform:
    """
    A class representing a Helmert transformation, which consists of a scaling factor, a rotation vector, and a
    translation vector. The transformation can be applied to a set of coordinates using the `apply` method.

    :param scale: The scaling factor. Default is 1.0.
    :type scale: float
    :param rotation: The rotation vector, as a list of three angles in degrees. Default is [0, 0, 0].

    """

    def __init__(
        self, scale: float = 0.0, rotation: List[float] = None, translation: List[float] = None, config: dict = None
    ):
        self.scale = scale
        self.rotation = np.array(rotation or [0, 0, 0], dtype=np.float64)
        self.translation = np.array(translation or [0, 0, 0], dtype=np.float64)
        if config is None:
            config = {}
        degrees = config.get("degrees", True)
        self.scaling_factor = config.get("scaling_factor", 1.0)
        self.scale *= self.scaling_factor
        if degrees:
            self.rotation = np.deg2rad(self.rotation)

    def __str__(self) -> str:
        np.set_printoptions(precision=4, suppress=True, formatter={"float": "{:0.4e}".format})
        return f"HelmertTransform(scale={self.scale/self.scaling_factor:.4e}, " \
               f"rotation={np.rad2deg(self.rotation)}, translation={self.translation})"
    
    def get_params(self) -> np.array:
        """
        Return the transformation parameters as a numpy array of shape (7,).

        :return: The transformation parameters.
        :rtype: numpy.array
        """
        return np.concatenate((self.translation, [self.scale], self.rotation))

    def as_rotation_matrix(self) -> np.array:
        """
        Return the rotation matrix corresponding to the rotation vector.

        :return: The rotation matrix, as a numpy array of shape (3, 3).
        :rtype: numpy.array
        """
        cos_angle = np.cos(self.rotation)
        sin_angle = np.sin(self.rotation)
        rot_x = np.array([[1, 0, 0], [0, cos_angle[0], -sin_angle[0]], [0, sin_angle[0], cos_angle[0]]])
        rot_y = np.array([[cos_angle[1], 0, sin_angle[1]], [0, 1, 0], [-sin_angle[1], 0, cos_angle[1]]])
        rot_z = np.array([[cos_angle[2], -sin_angle[2], 0], [sin_angle[2], cos_angle[2], 0], [0, 0, 1]])
        return rot_z @ rot_y @ rot_x

    def jac_rotation(self) -> (np.array, np.array, np.array):
        """
        jac_rotation the jacobian of the rotation matrix corresponding to the rotation vector.
        """
        cos_angle = np.cos(self.rotation)
        sin_angle = np.sin(self.rotation)
        rot_x = np.array([[1, 0, 0], [0, cos_angle[0], sin_angle[0]], [0, -sin_angle[0], cos_angle[0]]])
        rot_y = np.array([[cos_angle[1], 0, -sin_angle[1]], [0, 1, 0], [sin_angle[1], 0, cos_angle[1]]])
        rot_z = np.array([[cos_angle[2], sin_angle[2], 0], [-sin_angle[2], cos_angle[2], 0], [0, 0, 1]])
        rot_x_jac = np.array([[0, 0, 0], [0, -sin_angle[0], cos_angle[0]], [0, -cos_angle[0], -sin_angle[0]]])
        rot_y_jac = np.array([[-sin_angle[1], 0, -cos_angle[1]], [0, 0, 0], [cos_angle[1], 0, sin_angle[1]]])
        rot_z_jac = np.array([[-sin_angle[2], cos_angle[2], 0], [-cos_angle[2], -sin_angle[2], 0], [0, 0, 0]])
        return rot_z @ rot_y @ rot_x_jac, rot_z @ rot_y_jac @ rot_x, rot_z_jac @ rot_y @ rot_x

    def apply(self, data: np.array) -> np.array:
        """
        Apply the Helmert transformation to a set of coordinates.

        :param data: The coordinates to transform, as a numpy array of shape (n, 3).
        :type data: numpy.array
        :return: The transformed coordinates, as a numpy array of shape (n, 3).
        :rtype: numpy.array
        """
        data = np.array(data, dtype=np.float64)
        return (1 + self.scale) * (data @ self.as_rotation_matrix().T) + self.translation

    def jacobian(self, data: np.array, params=None) -> np.array:
        """
        Return the Jacobian matrix of the Helmert transformation.

        :param data: The coordinates to transform, as a numpy array of shape (n, 3).
        :type data: numpy.array
        :return: The Jacobian matrix, as a numpy array of shape (7, n, 3).
        :rtype: numpy.array
        """
        if params is None:
            params = {"translation": True, "rotation": True, "scale": True}
        data = np.array(data, dtype=np.float64)
        rot_jac = self.jac_rotation()
        rot = self.as_rotation_matrix()
        translation_jac = np.eye(3)
        n_param = 0
        if params["translation"]:
            n_param += 3
        if params["rotation"]:
            n_param += 3
        if params["scale"]:
            n_param += 1
        jacobian = np.zeros((data.shape[0], 3, n_param))
        print(jacobian.shape)
        idx = 0
        if params["translation"]:
            jacobian[:, :, :3] = np.tile(translation_jac, (data.shape[0], 1, 1))
            idx += 3
        if params["scale"]:
            jacobian[:, :, idx] = data @ rot
            idx += 1
        if params["rotation"]:
            jacobian[:, :, idx] = data @ rot_jac[0] * (1 + self.scale)
            jacobian[:, :, idx + 1] = data @ rot_jac[1] * (1 + self.scale)
            jacobian[:, :, idx + 2] = data @ rot_jac[2] * (1 + self.scale)
        return jacobian

    def fit(self, data: np.array, target: np.array, params: dict = None) -> np.array:
        """
        Fit the Helmert transformation to a set of coordinates.

        :param data: The coordinates to transform, as a numpy array of shape (n, 3).
        :type data: numpy.array
        :param target: The target coordinates, as a numpy array of shape (n, 3).
        :type target: numpy.array
        :param params: A dictionary containing the parameters to fit. Default is {'translation': True, 'rotation': True, 'scale': True}.
        :type params: dict
        :return: The fitted transformation parameters, as a numpy array of shape (7,).
        :rtype: numpy.array
        """
        if params is None:
            params = {"translation": True, "rotation": True, "scale": True}
        residuals = self.apply(data) - target
        design = self.jacobian(data, params)
        residuals = residuals.reshape(-1)
        design = design.reshape((design.shape[0] * design.shape[1], -1))
        delta = np.linalg.inv(design.transpose() @ design) @ design.transpose() @ residuals
        idx = 0
        if params["translation"]:
            self.translation -= delta[:3]
            idx += 3
        if params["scale"]:
            self.scale -= delta[idx]
            idx += 1
        if params["rotation"]:
            self.rotation -= delta[idx:]
