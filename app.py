import streamlit as st
from typing import Dict, List

# --- Session State Setup ---
if "players" not in st.session_state:
    st.session_state.players = {}  # {code: {name, personality, action, inbox}}
if "history" not in st.session_state:
    st.session_state.history = ["Bem-vindos ao reality show com IA!"]
if "theme" not in st.session_state:
    st.session_state.theme = ""

st.title("🏝 Reality Show IA – Drama Total")

# 1) Definir tema
if not st.session_state.theme:
    st.session_state.theme = st.text_input(
        "Define o tema (ex: Reality show estilo Drama Total):"
    )
    st.stop()

# 2) Entrar na sessão
code = st.text_input("Código da sessão", max_chars=4).upper()
name = st.text_input("Nome do jogador")
personality = st.text_input("Personalidade breve")
if st.button("Juntar-me"):
    if code and name and personality:
        st.session_state.players.setdefault(code, {
            "name": name,
            "personality": personality,
            "action": "",
            "inbox": []
        })
        st.experimental_rerun()
    else:
        st.error("Preenche tudo para entrar.")

# 3) Zona de jogo
if code in st.session_state.players:
    player = st.session_state.players[code]
    st.markdown(f"**Tema:** {st.session_state.theme}")
    st.markdown("**História atual:**")
    st.write("\n\n".join(st.session_state.history))

    # 3a) Mensagem secreta
    to = st.selectbox("Enviar mensagem secreta a", 
                      options=[p for p in st.session_state.players if p!=code] + ["—"])
    msg = st.text_area("Mensagem secreta (opcional)")
    action = st.text_area("Ação do teu personagem")

    if st.button("Terminar turno"):
        player["action"] = action
        if to!="—" and msg:
            st.session_state.players[to]["inbox"].append(f"De {player['name']}: {msg}")
        # Check se todos jogaram
        if all(p["action"] for p in st.session_state.players.values()):
            # Gerar novo trecho (simples placeholder)
            novo = f"- {', '.join(p['name'] + ' ' + p['action'] for p in st.session_state.players.values())}"
            st.session_state.history.append(novo)
            for p in st.session_state.players.values():
                p["action"] = ""
            st.experimental_rerun()
        else:
            st.success("Ações registadas. Aguardar os outros jogadores.")
        st.experimental_rerun()

    # Caixa de entrada
    if player["inbox"]:
        st.markdown("**Caixa de mensagens secretas:**")
        for m in player["inbox"]:
            st.info(m)

    st.stop()
