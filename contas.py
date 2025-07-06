import psycopg2

class Conta:
    
    def __init__(self, id: int, name: str, password: str, email: str, foto_perfil: str = None, banner: str = None ,sobre: str = None):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.foto_perfil = foto_perfil
        self.banner = banner
        self.sobre = sobre
        
    def set_id(self,novo_id):
        self.id = novo_id
    
    def to_dict(self):      
        return {
            'id': str(self.id),
            'nome': self.name,
            'email': self.email,
            'fotoPerfil': self.foto_perfil,
            'banner': self.banner,
            'sobre': self.sobre
        }

class Perfil_Pessoal(Conta):
    
    def __init__(self, id: int, name: str, email: str, password: str, titulo: str, **kwargs):
        super().__init__(id=id,name=name,email=email, password=password, **kwargs)
        self.titulo = titulo
        self.tipo = "pessoal"
    
    def to_dict(self):
        data = super().to_dict()
        data['titulo'] = self.titulo
        data['tipo'] = 'pessoal'
        return data
        
class Perfil_Empresarial(Conta):
    
    def __init__(self, id: int, name: str, email: str, password: str, nome_fantasia: str, localizacao: str, setor: str, cod_institucional: int = None, **kwargs):
        super().__init__(id=id,name=name, email=email, password=password, **kwargs)
        self.nome_fantasia = nome_fantasia  
        self.localizacao = localizacao  
        self.setor = setor
        self.cod_institucional = cod_institucional
        self.tipo = "empresarial"
    def to_dict(self):
        data = super().to_dict()
        data['nomeFantasia'] = self.nome_fantasia
        data['localizacao'] = self.localizacao
        data['setor'] = self.setor
        data['tipo'] = 'empresarial'
        return data
    

class Gerenciamento_Contas:
    
    def __init__(self,conexao):
        self.conexao = conexao
        
    
    def login(self, user, password) -> Conta:
        
        try:
            with self.conexao.cursor() as cursor:
                consulta = """
                    SELECT * FROM contas
                    WHERE email = %s AND senha = %s
                """
                cursor.execute(consulta, (user, password))
                conta = cursor.fetchone()

                if not conta:
                    print("Usuário ou senha incorretos.")
                    return None

                conta_id, email, nome, senha, foto_perfil, banner, sobre = conta

                cursor.execute("SELECT titulo FROM perfil_p WHERE cid = %s", (conta_id,))
                perfil_p = cursor.fetchone()

                if perfil_p:
                    return Perfil_Pessoal(
                        id=conta_id, name=nome, email=email, password=senha,
                        titulo=perfil_p[0],
                        foto_perfil=foto_perfil, banner=banner, sobre=sobre
                    )

                # Verifica se é perfil empresarial
                cursor.execute("""
                    SELECT NomeFantasia, Localizacao, ID_setor, Cod_institucional
                    FROM perfil_emp
                    WHERE cid = %s
                """, (conta_id,))
                perfil_emp = cursor.fetchone()

                if perfil_emp:
                    nome_fantasia, localizacao, setor, cod_institucional = perfil_emp
                    return Perfil_Empresarial(
                        id=conta_id, name=nome, email=email, password=senha,
                        nome_fantasia=nome_fantasia, localizacao=localizacao,
                        setor=setor, cod_institucional=cod_institucional,
                        foto_perfil=foto_perfil, banner=banner, sobre=sobre
                    )

                print("Conta sem perfil vinculado.")
                return None

        except psycopg2.Error as e:
            print("Erro ao acessar o banco de dados:", e)
            return None
            
    
    def criar_conta(self, data: dict):
        
        nova_conta = self.gerar_conta(data)
        
        if nova_conta is not None:
            try:
                nova_conta = self.insert_conta_banco(nova_conta)  
                self.conexao.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                self.conexao.rollback()
                print(f"Falha ao inserir conta no banco de dados: {e}")
    
    def insert_conta_banco(self, conta):
        
        with self.conexao.cursor() as cursor:
            
            cursor.execute("""
                INSERT INTO contas (Email, Nome, Senha, Foto_Perfil, Banner, Sobre) 
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                conta.email, conta.name, conta.password,
                conta.foto_perfil, conta.banner, conta.sobre
            ))
            
            conta_id = cursor.fetchone()[0]
            conta.set_id(conta_id)
            
            if conta.tipo == "pessoal":
                
                cursor.execute("""
                    INSERT INTO perfil_p (titulo, cid)
                    VALUES (%s, %s)
                """, (conta.titulo, conta.id))
                
            elif conta.tipo == "empresarial": 
                
                cursor.execute("""
                    INSERT INTO perfil_emp (CId, NomeFantasia, Localizacao, ID_setor, Cod_institucional)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    conta.id, conta.nome_fantasia, conta.localizacao,
                    conta.setor, conta.cod_institucional
                ))
                
        
            
    
    def gerar_conta(self, data: dict):
        
        tipo_conta = data['tipo']
        nova_conta = None
        
        try:
            if tipo_conta == "pessoal":
                nova_conta = Perfil_Pessoal(
                    id = 0, # Id sera gerado inicialmente pelo banco
                    name=data['name'],
                    email=data['email'],
                    password=data['password'],
                    titulo=data['titulo'],
                    foto_perfil=data.get('foto_perfil'),
                    banner=data.get('banner'),
                    sobre=data.get('sobre')
                )
            
            elif tipo_conta == "empresarial":
                nova_conta = Perfil_Empresarial(
                    id = 0, # Id sera gerado inicialmente pelo banco
                    name=data['name'],
                    email=data['email'],
                    password=data['password'],
                    nome_fantasia=data['nome_fantasia'],
                    localizacao=data['localizacao'],
                    setor=data['setor'],
                    foto_perfil=data.get('foto_perfil'),
                    banner=data.get('banner'),
                    sobre=data.get('sobre'),
                    cod_institucional=data.get('cod_institucional')
                )
            else:
                return (None)
            return (nova_conta)
        except KeyError as e:
            print(f"Campo ausente: {e}")
            return (None)