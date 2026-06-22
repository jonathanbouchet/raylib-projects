#version 330

in vec2 fragTexCoord;
uniform sampler2D texture0;
out vec4 finalColor;

void main(){
    // 0. white out the full texture
    //finalColor = vec4(1.0, 1.0, 1.0, 1.0); white out the full texture

    // 1. white out only the texture
    // vec4 texelColor = texture(texture0, fragTexCoord);
    // finalColor = vec4(1.0, 1.0, 1.0, texelColor.a);

    // 2. gray shader
    // Calculate grayscale (Luminance)
    vec4 texelColor = texture(texture0, fragTexCoord);
    float gray = dot(texelColor.rgb, vec3(0.299, 0.587, 0.114));
    // Final color with tint and grayscale applied
    finalColor = vec4(gray, gray, gray, texelColor.a);
}