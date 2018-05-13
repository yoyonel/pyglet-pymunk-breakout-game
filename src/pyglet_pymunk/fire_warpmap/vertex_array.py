from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy, math
from PIL import Image


class StereoDepth(object):
    # constants
    BACKGROUND_IMAGE = 'datas/cooling_map.png'

    # vertex shader program
    vertexShader = """
        #version 330 core

        attribute vec3 vert;
        attribute vec2 uV;
        uniform mat4 mvMatrix;
        uniform mat4 pMatrix;
        out vec2 UV;

        void main() {
          gl_Position = pMatrix * mvMatrix * vec4(vert, 1.0);
          UV = uV;
        }
    """

    # fragment shader program
    fragmentShader = """
        #version 330 core

        in vec2 UV;
        uniform sampler2D backgroundTexture;
        out vec3 colour;

        void main() {
          colour = texture(backgroundTexture, UV).r * vec3(1) * 16;
        }
    """
    def __init__(self):
        self.uvBuffer = None
        self._init_opengl()

        # initialise opengl
    def _init_opengl(self):
        # create shader program
        vs = compileShader(self.vertexShader, GL_VERTEX_SHADER)
        fs = compileShader(self.fragmentShader, GL_FRAGMENT_SHADER)
        self.program = compileProgram(vs, fs)
        glUseProgram(self.program)

        # obtain uniforms and attributes
        aVert = glGetAttribLocation(self.program, "vert")
        aUV = self.aUV = glGetAttribLocation(self.program, "uV")
        self.uPMatrix = glGetUniformLocation(self.program, 'pMatrix')
        self.uMVMatrix = glGetUniformLocation(self.program, "mvMatrix")
        self.uBackgroundTexture = glGetUniformLocation(self.program, "backgroundTexture")

        # set background vertex
        backgroundVertex = [
            -2.0, 1.5, -3.6,
            -2.0, -1.5, -3.6,
            2.0, 1.5, -3.6,
            2.0, 1.5, -3.6,
            -2.0, -1.5, -3.6,
            2.0, -1.5, -3.6]

        # set background UV
        backgroundUV = [
            0.0, 0.0,
            0.0, 1.0,
            1.0, 0.0,
            1.0, 0.0,
            0.0, 1.0,
            1.0, 1.0]

        # create and bind VAO
        self.backgroundVAO = glGenVertexArrays(1)
        glBindVertexArray(self.backgroundVAO)

        # generate vertex buffer
        vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)

        # enable vertex attribute array
        glEnableVertexAttribArray(aVert)

        # vertex attribute pointer
        glVertexAttribPointer(aVert, 3, GL_FLOAT, GL_FALSE, 0, None)

        # buffer vertex data
        vertexData = numpy.array(backgroundVertex, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertexData), vertexData, GL_STATIC_DRAW)

        # generate UV buffer
        uvBuffer = glGenBuffers(1)
        self.uvBuffer = uvBuffer
        glBindBuffer(GL_ARRAY_BUFFER, uvBuffer)

        # enable UV attribute array
        glEnableVertexAttribArray(aUV)

        # UV attribute pointer
        glVertexAttribPointer(aUV, 2, GL_FLOAT, GL_FALSE, 0, None)

        # buffer UV data
        self.uvData = numpy.array(backgroundUV, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(self.uvData), self.uvData, GL_STATIC_DRAW)

        # unbind and disable
        glBindVertexArray(0)
        glDisableVertexAttribArray(aVert)
        glDisableVertexAttribArray(aUV)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # # set background texture
        backgroundImage = Image.open(self.BACKGROUND_IMAGE)
        backgroundImageData = numpy.array(list(backgroundImage.getdata()), numpy.uint8)
        #
        self.backgroundTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.backgroundTexture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, backgroundImage.size[0], backgroundImage.size[1], 0, GL_RED,
                     GL_UNSIGNED_BYTE, backgroundImageData)
        glBindTexture(GL_TEXTURE_2D, 0)

    # draw frame
    def _draw_frame(self):
        # create modelview matrix
        mvMatrix = numpy.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0], numpy.float32)

        # create projection matrix
        fov = math.radians(45.0)
        f = 1.0 / math.tan(fov / 2.0)
        zNear = 0.1
        zFar = 100.0
        # aspect = glutGet(GLUT_WINDOW_WIDTH) / float(glutGet(GLUT_WINDOW_HEIGHT))
        aspect = 1.0
        pMatrix = numpy.array([
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0, (zFar + zNear) / (zNear - zFar), -1.0,
            0.0, 0.0, 2.0 * zFar * zNear / (zNear - zFar), 0.0], numpy.float32)

        data = numpy.random.rand(len(self.uvData))
        glBindBuffer(GL_ARRAY_BUFFER, self.uvBuffer)
        glBufferSubData(GL_ARRAY_BUFFER, 0, 4 * len(data), data)

        # use shader program
        glUseProgram(self.program)

        # set uniforms
        glUniformMatrix4fv(self.uMVMatrix, 1, GL_FALSE, mvMatrix)
        glUniformMatrix4fv(self.uPMatrix, 1, GL_FALSE, pMatrix)
        glUniform1i(self.uBackgroundTexture, 0)

        # bind VAO
        glBindVertexArray(self.backgroundVAO)

        # bind background texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.backgroundTexture)

        # draw
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # unbind
        glBindVertexArray(0)
        glUseProgram(0)

        # swap buffers
        # glutSwapBuffers()

    # setup and run OpenGL
    # def main(self):
        # glutInit()
        # glutInitWindowSize(640, 480)
        # glutInitWindowPosition(100, 100)
        # glutCreateWindow('Stereo Depth')
        # glutDisplayFunc(self._draw_frame)
        # self._init_opengl()
        # glutMainLoop()


if __name__ == '__main__':
    # run an instance of StereoDepth
    StereoDepth().main()
