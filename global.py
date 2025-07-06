Query_map = {
    '1': '''
        SELECT
            s.Nome AS nome_setor,
            MAX(v.salario) AS maior_salario_oferecido 
        FROM
            Setor s
        JOIN
            Perfil_emp pe ON s.id = pe.ID_setor
        JOIN
            Vagas v ON pe.CId = v.empresa_id
        WHERE
            v.status = 'Aberta'
            AND v.salario IS NOT NULL
        GROUP BY
            s.Nome
        ORDER BY
            maior_salario_oferecido DESC;
    ''',

    '2': '''
        SELECT DISTINCT
            pe.NomeFantasia
        FROM
            Seguir s
        JOIN
            Perfil_emp pe ON s.ID_emp = pe.CId
        WHERE
            s.ID_pessoa IN (
                SELECT ID_pessoa_rec FROM Conectar WHERE ID_pessoa_emi = %s
                UNION
                SELECT ID_pessoa_emi FROM Conectar WHERE ID_pessoa_rec = %s
            )
        ORDER BY
            pe.NomeFantasia;
    ''',
    
    '3': '''
        SELECT
            v.id_pessoa,
            v.nome_pessoa,
            v.Titulo
        FROM
            vw_PerfilPessoalCompleto v
        WHERE
            NOT EXISTS (
                SELECT 1
                FROM
                    Necessita_qualificacao nq
                WHERE
                    nq.ID_vaga = %s
                    AND NOT EXISTS (
                        SELECT 1
                        FROM
                            Possuir_qualificacao pq
                        WHERE
                            pq.ID_pessoa = v.id_pessoa
                            AND pq.ID_qualificacao = nq.ID_qualificacao
                    )
            );
    ''',
    
    '4': '''
        SELECT
            v.id_pessoa,
            v.nome_pessoa,
            v.Titulo AS titulo_atual
        FROM
            vw_PerfilPessoalCompleto v
        WHERE
            v.id_pessoa IN (
                (
                    SELECT ep.ID_pessoa
                    FROM Experiencia_profissional ep
                    JOIN Perfil_emp pe_empresa ON ep.ID_emp = pe_empresa.CId
                    WHERE pe_empresa.CId = %s
                )
                INTERSECT
                (
                    SELECT ea.ID_pessoa
                    FROM Exp_Academica ea
                    JOIN Perfil_emp pe_instituicao ON ea.ID_emp = pe_instituicao.cid 
                    WHERE pe_instituicao.CId = %s
                )
            )
        ORDER BY
            v.nome_pessoa;
    ''',
    
    '5': '''
        SELECT DISTINCT
            v.id_pessoa,
            v.nome_pessoa,
            v.Titulo AS titulo_perfil
        FROM
            vw_PerfilPessoalCompleto v
        JOIN
            Candidatos c ON v.id_pessoa = c.ID_pessoa
        WHERE
            NOT EXISTS (
                SELECT 1
                FROM Certificacoes ce 
                WHERE
                    ce.ID_perfil = v.id_pessoa
                    AND ce.Titulo = %s
            )
        ORDER BY
            v.nome_pessoa;
    ''',
    
    '6': '''
        SELECT
            pe.NomeFantasia AS nome_instituicao,
            COUNT(DISTINCT ea.ID_pessoa) AS quantidade_de_formados
        FROM
            Exp_Academica ea
        JOIN
            vw_InstituicoesEnsino pe ON ea.ID_emp = pe.id_conta
        JOIN
            Perfil_p pp ON ea.ID_pessoa = pp.CId
        WHERE
            EXTRACT(YEAR FROM ea.date_fim) = %s
            AND pp.Titulo LIKE %s
        GROUP BY
            pe.NomeFantasia
        HAVING
            COUNT(DISTINCT ea.ID_pessoa) > %s
        ORDER BY
            quantidade_de_formados DESC;
    ''',
    '7': '''
        SELECT DISTINCT
            vg.titulo,
            vg.vaga_id
        FROM
            vagas vg
        JOIN
            candidatos USING (vaga_id)
        WHERE
            candidatos.ID_pessoa IN (
                SELECT ID_pessoa_rec FROM Conectar WHERE ID_pessoa_emi = %s
                UNION
                SELECT ID_pessoa_emi FROM Conectar WHERE ID_pessoa_rec = %s
            )
        ORDER BY titulo;
    ''',
    
    '8': '''
        SELECT
            pe.NomeFantasia AS nome_instituicao,
            COUNT(DISTINCT ep.ID_pessoa) AS total_formandos_contratados
        FROM
            Experiencia_profissional ep
        JOIN
            Exp_Academica ea ON ep.ID_pessoa = ea.ID_pessoa
        JOIN
            Perfil_emp pe ON ea.ID_emp = pe.CId
        WHERE
            ep.Data_Fim IS NULL
        GROUP BY
            pe.NomeFantasia
        ORDER BY
            total_formandos_contratados DESC;
    ''',
    
    '9': '''
        SELECT
            v.nome_pessoa,
            COALESCE(cl.qtd_curtidas, 0) AS total_de_curtidas,
            COALESCE(cc.qtd_comentarios, 0) AS total_de_comentarios
        FROM
            Participantes p 
        JOIN
            vw_PerfilPessoalCompleto v ON p.ID_participante = v.id_pessoa
        LEFT JOIN (
            SELECT
                ID_conta,
                COUNT(*) AS qtd_curtidas
            FROM Curtidas
            GROUP BY ID_conta
        ) AS cl ON v.id_pessoa = cl.ID_conta
        LEFT JOIN (
            SELECT
                ID_pessoa,
                COUNT(*) AS qtd_comentarios
            FROM Comentar
            GROUP BY ID_pessoa
        ) AS cc ON v.id_pessoa = cc.ID_pessoa
        WHERE
            p.ID_grupo = %s
        ORDER BY
            v.nome_pessoa;
    ''',
    
    '10': '''
        SELECT
            pe.NomeFantasia AS nome_da_empresa,
            v.titulo AS titulo_da_vaga,
            v.modalidade,
            q.Nome AS qualificacao_necessaria
        FROM
            Vagas v
        JOIN
            Perfil_emp pe ON v.empresa_id = pe.CId
        LEFT JOIN
            Necessita_qualificacao nq ON v.vaga_id = nq.ID_vaga
        LEFT JOIN
            Qualificacoes q ON nq.ID_qualificacao = q.id
        WHERE
            pe.cid  = %s
            AND v.modalidade = %s
            AND v.status = %s
        ORDER BY
            v.titulo,
            qualificacao_necessaria;
    '''

    
}