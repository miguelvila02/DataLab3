"""
Testes para o modelo de previsão.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adiciona a diretoria src ao sys.path para importar módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


from server.modelbuild.make_prediction import (
    predict_from_recent_form,
    calculate_avg_stats,
    predict_with_custom_weights,
)

# Fixtures


@pytest.fixture
def sample_home_games():
    return [
        {"possession": 55.0, "shots_on_target": 7, "corners": 5, "fouls": 10},
        {"possession": 60.0, "shots_on_target": 8, "corners": 6, "fouls": 12},
        {"possession": 50.0, "shots_on_target": 5, "corners": 4, "fouls": 8},
        {"possession": 58.0, "shots_on_target": 9, "corners": 7, "fouls": 11},
        {"possession": 62.0, "shots_on_target": 10, "corners": 8, "fouls": 9},
    ]


@pytest.fixture
def sample_away_games():
    return [
        {"possession": 45.0, "shots_on_target": 4, "corners": 3, "fouls": 14},
        {"possession": 48.0, "shots_on_target": 6, "corners": 4, "fouls": 13},
        {"possession": 52.0, "shots_on_target": 5, "corners": 5, "fouls": 15},
        {"possession": 47.0, "shots_on_target": 7, "corners": 6, "fouls": 12},
        {"possession": 50.0, "shots_on_target": 4, "corners": 4, "fouls": 16},
    ]


@pytest.fixture
def balanced_weights():
    return [{"possession": 50.0, "shots_on_target": 4, "corners": 5, "fouls": 11} for _ in range(5)]


# Testar casos
class TestCalculateAvgStats:
    """Testes para a função calculate_avg_stats."""

    def test_calculate_avg_stats(self, sample_home_games):
        result = calculate_avg_stats(sample_home_games)

        assert "avg_possession" in result
        assert "avg_shots_on_target" in result
        assert "avg_corners" in result
        assert "avg_fouls" in result

        # Verifica os valores calculados
        assert 50 <= result["avg_possession"] <= 60
        assert 3 <= result["avg_shots_on_target"] <= 7
        assert 4 <= result["avg_corners"] <= 8
        assert 8 <= result["avg_fouls"] <= 12

    def test_single_game_stats(self):
        single_game = [{"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10}]
        result = calculate_avg_stats(single_game)

        assert result["avg_possession"] == 55.0
        assert result["avg_shots_on_target"] == 5.0
        assert result["avg_corners"] == 6.0
        assert result["avg_fouls"] == 10.0

    def test_empty_game_list(self):
        with pytest.raises(ValueError, match="A lista de jogos não pode estar vazia."):
            calculate_avg_stats([])


class TestPredictFromRecentForm:
    """Testes para a função predict_from_recent_form."""

    def test_prediction_structure(self, sample_home_games, sample_away_games):
        """Testa se a estrutura do resultado da previsão está correta."""
        result = predict_from_recent_form(sample_home_games, sample_away_games)

        # Verifica se todas as chaves esperadas estão presentes
        assert "prediction" in result
        assert "prediction_code" in result
        assert "probabilities" in result
        assert "confidence" in result
        assert "home_team_averages" in result
        assert "away_team_averages" in result

    def test_prediction_values(self, sample_home_games, sample_away_games):
        """Testa os valores retornados pela previsão."""
        result = predict_from_recent_form(sample_home_games, sample_away_games)

        # Outcomes da previsão
        assert result["prediction"] in ["Home Win", "Draw", "Away Win"]
        assert result["prediction_code"] in [1, 0, -1]

        # Confiança
        assert 0 <= result["confidence"] <= 100

    def test_probabilities_sum_to_one(self, sample_home_games, sample_away_games):
        """Testa se as probabilidades somam 1."""
        result = predict_from_recent_form(sample_home_games, sample_away_games)

        prob_sum = sum(result["probabilities"].values())
        assert abs(prob_sum - 1.0) < 0.01  # Allow small floating point error

    def test_probabilities_all_positive(self, sample_home_games, sample_away_games):
        """Testa se todas as probabilidades são positivas."""
        result = predict_from_recent_form(sample_home_games, sample_away_games)

        for prob in result["probabilities"].values():
            assert prob >= 0
            assert prob <= 1

    def test_balanced_teams(self, balanced_weights):
        """Testa o caso onde ambas as equipes têm desempenhos equilibrados."""
        result = predict_with_custom_weights(balanced_weights, balanced_weights)

        # Com estatísticas idênticas o outcome nao pode ser 100% previsível
        assert result["confidence"] < 90


class TestPredictWithCustomWeights:
    """Testes para a função predict_with_custom_weights."""

    def test_default_weights(self, sample_home_games, sample_away_games):
        # Testa a previsão com pesos padrão
        result = predict_with_custom_weights(sample_home_games, sample_away_games)

        assert "weights_used" in result
        assert len(result["weights_used"]) == 5  # possession, shots_on_target, corners, fouls
        assert abs(sum(result["weights_used"]) - 1.0) < 0.01  # Deve somar 1

    def test_custom_weights(self, sample_home_games, sample_away_games):
        # Testa a previsão com pesos personalizados
        custom_weights = [0.05, 0.1, 0.15, 0.30, 0.4]
        result = predict_with_custom_weights(
            sample_home_games, sample_away_games, weights=custom_weights
        )

        # Verifica se os pesos usados estão normalizados
        assert abs(sum(result["weights_used"]) - 1.0) < 0.01

    def test_equal_weights(self, sample_home_games, sample_away_games):
        # Testa a previsão com pesos iguais
        equal_weights = [0.2, 0.2, 0.2, 0.2, 0.2]

        result_weighted = predict_with_custom_weights(
            sample_home_games, sample_away_games, weights=equal_weights
        )

        result_simple = predict_with_custom_weights(sample_home_games, sample_away_games)

        # Previsões devem ser semelhantes, mas um pouco diferentes devido à aleatoriedade do modelo
        for key in result_simple["home_team_averages"].keys():
            diff = abs(
                result_weighted["home_team_averages"][key]
                - result_simple["home_team_averages"][key]
            )
            assert diff < 5.0  # Diferença pequena nas médias calculadas permitida

        def test_invalid_weights_length(self, sample_home_games, sample_away_games):
            # Testa se um erro é levantado quando o comprimento dos pesos é inválido
            invalid_weights = [0.5, 0.5]  # apenas 2 pesos em vez de 5

            with pytest.raises(ValueError, match="Weights length must match number of games"):
                predict_with_custom_weights(
                    sample_home_games, sample_away_games, weights=invalid_weights
                )


class TestEdgeCases:
    """Testes para casos extremos."""

    def test_extreme_dominance_home(self):
        """Testa o caso onde a equipa da casa domina completamente."""
        dominant_home = [
            {"possession": 70.0, "shots_on_target": 10, "corners": 12, "fouls": 5} for _ in range(5)
        ]
        weak_away = [
            {"possession": 30.0, "shots_on_target": 1, "corners": 2, "fouls": 18} for _ in range(5)
        ]

        result = predict_from_recent_form(dominant_home, weak_away)

        # A previsão deve ser vitória em casa com alta confiança
        assert result["probabilities"]["Home Win"] > 0.4

    def test_extreme_dominance_away(self):
        """Testa o caso onde a equipa visitante domina completamente."""
        weak_home = [
            {"possession": 30.0, "shots_on_target": 1, "corners": 2, "fouls": 18} for _ in range(5)
        ]
        dominant_away = [
            {"possession": 70.0, "shots_on_target": 10, "corners": 12, "fouls": 5} for _ in range(5)
        ]

        result = predict_from_recent_form(weak_home, dominant_away)

        # A previsão deve ser vitória fora com alta confiança
        assert result["probabilities"]["Away Win"] > 0.3

    def test_different_game_counts(self):
        """Testa o caso onde as equipas têm diferentes números de jogos recentes."""
        for n_games in [1, 3, 5, 7, 10]:
            home_games = [
                {"possession": 55.0, "shots_on_target": 5, "corners": 4, "fouls": 10}
                for i in range(n_games)
            ]
            away_games = [
                {"possession": 45.0, "shots_on_target": 5, "corners": 4, "fouls": 10 + i}
                for i in range(n_games)
            ]

            result = predict_from_recent_form(home_games, away_games)

            assert result is not None
            assert "prediction" in result


# Parametrizar os testes
@pytest.mark.parametrize(
    "possession,expected_range",
    [
        (70.0, (60.0, 80.0)),
        (50.0, (40.0, 60.0)),
        (30.0, (20.0, 40.0)),
    ],
)
def test_possession_ranges(possession, expected_range):
    """Testa se os valores da posse de bola estão dentro dos intervalos esperados."""
    games = [
        {"possession": possession, "shots_on_target": 5, "corners": 5, "fouls": 10}
        for _ in range(5)
    ]

    result = calculate_avg_stats(games)
    avg_possession = result["avg_possession"]

    assert expected_range[0] <= avg_possession <= expected_range[1]


@pytest.mark.parametrize(
    "shots_on_target,expected_min",
    [
        (10, 8),
        (5, 4),
        (1, 0.5),
    ],
)
def test_shots_on_target_minimums(shots_on_target, expected_min):
    """Testa se os remates à baliza estão na avaliada mínima esperada(target)."""
    games = [
        {"possession": 50.0, "shots_on_target": shots_on_target, "corners": 5, "fouls": 10}
        for _ in range(5)
    ]

    result = calculate_avg_stats(games)
    avg_shots = result["avg_shots_on_target"]

    assert avg_shots >= expected_min


# Integração dos testes com o modelo de previsão
class TestIntegrationWithModel:
    """Testes de integração com o modelo de previsão."""

    def test_full_prediction_pipeline(self, sample_home_games, sample_away_games):
        """Testa a pipeline de previsão completa."""
        # Calcula médias
        home_avg = calculate_avg_stats(sample_home_games)
        away_avg = calculate_avg_stats(sample_away_games)

        # Faz a previsão
        result = predict_from_recent_form(sample_home_games, sample_away_games)

        # Verifica médias calculadas
        for key in home_avg.keys():
            assert result["home_team_averages"][key] == home_avg[key]

        for key in away_avg.keys():
            assert result["away_team_averages"][key] == away_avg[key]

        # Verifica se a previsão é válida
        assert result["prediction"] in ["Home Win", "Draw", "Away Win"]
        assert 0 <= result["confidence"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/server/model", "--cov-report=html"])
