#Definition of the Shaders: Vertex Code and Fragment Code

vertex = """
    attribute vec3 position;
    attribute vec2 texture_coord;
    attribute vec3 normals;

    varying vec2 out_texture;
    varying vec3 out_fragPos;
    varying vec3 out_normal;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;        
    void main(){
        gl_Position = projection * view * model * vec4(position,1.0);
        out_texture = vec2(texture_coord);
        out_fragPos = vec3(model * vec4(position, 1.0));
        out_normal = normals;            
    }
    """

fragment = """

    // parametros da iluminacao ambiente e difusa
    uniform vec3 lightPos; // define coordenadas de posicao da luz #1
    
    // parametros da iluminacao especular
    uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
    
    // parametro com a cor da(s) fonte(s) de iluminacao
    vec3 lightColor = vec3(1.0, 1.0, 1.0);

    // parametros recebidos do vertex shader
    varying vec2 out_texture; // recebido do vertex shader
    varying vec3 out_normal; // recebido do vertex shader
    varying vec3 out_fragPos; // recebido do vertex shader
    uniform sampler2D samplerTexture;
    
    
    
    void main(){
    
        // calculando reflexao ambiente
        vec3 ambient = 0.2 * lightColor;             
    
        ////////////////////////
        // Luz #1
        ////////////////////////
        
        // calculando reflexao difusa
        vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
        vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
        float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
        vec3 diffuse = 0.2 * diff * lightColor; // iluminacao difusa
        
        // calculando reflexao especular
        vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
        vec3 reflectDir = reflect(-lightDir, norm); // direcao da reflexao
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64.0);
        vec3 specular = 0.8 * spec * lightColor;    
        
        
        ////////////////////////
        // Combinando as duas fontes
        ////////////////////////
        
        // aplicando o modelo de iluminacao
        vec4 texture = texture2D(samplerTexture, out_texture);
        vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
        gl_FragColor = result;
    }
        """
