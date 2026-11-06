"""Probability simulation and statistical inference using labelled synthetic data."""
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats

SEED = 42


def mean_interval(values, confidence=0.95):
    """Two-sided Student t interval for a finite, independent numeric sample."""
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size < 2 or not np.all(np.isfinite(values)):
        raise ValueError('Expected at least two finite values in a 1D sample.')
    if not 0 < confidence < 1:
        raise ValueError('Confidence must be between zero and one.')
    mean = float(np.mean(values))
    margin = stats.t.ppf((1 + confidence) / 2, len(values) - 1) * stats.sem(values)
    return [float(mean - margin), float(mean + margin)]


def experiment():
    rng = np.random.default_rng(SEED)
    # P(at least 4 heads in 5 fair tosses), simulated and computed analytically.
    tosses = rng.binomial(5, 0.5, size=100_000)
    simulated = float(np.mean(tosses >= 4))
    exact = float(stats.binom.sf(3, 5, 0.5))
    # Artificial populations: these are not Spotify or salary observations.
    group_a = rng.normal(50, 10, 200)
    group_b = rng.normal(54, 12, 180)
    test = stats.ttest_ind(group_a, group_b, equal_var=False)
    means = rng.exponential(scale=2, size=(5_000, 40)).mean(axis=1)
    report = {
        'data': 'Synthetic data only; no claims about real people or music.',
        'seed': SEED, 'binomial_trials': len(tosses),
        'binomial_simulated_probability': simulated,
        'binomial_exact_probability': exact,
        'monte_carlo_standard_error': float(np.sqrt(exact * (1 - exact) / len(tosses))),
        'group_a': {'n': len(group_a), 'mean': float(group_a.mean()),
                    'sample_std': float(group_a.std(ddof=1)), 'mean_ci_95': mean_interval(group_a)},
        'group_b': {'n': len(group_b), 'mean': float(group_b.mean()),
                    'sample_std': float(group_b.std(ddof=1)), 'mean_ci_95': mean_interval(group_b)},
        'welch_t': float(test.statistic), 'welch_p': float(test.pvalue),
        'alpha': 0.05, 'reject_equal_means': bool(test.pvalue < 0.05),
        'clt': {'replications': len(means), 'sample_size': 40, 'population_mean': 2,
                'observed_mean_of_means': float(means.mean())},
        'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
    }
    return report, tosses, group_a, group_b, means


def main():
    output = Path(__file__).resolve().parents[1] / 'reports'
    output.mkdir(exist_ok=True)
    report, tosses, group_a, group_b, means = experiment()
    (output / 'statistics.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].hist(tosses, bins=np.arange(-0.5, 6.5, 1), density=True, rwidth=0.8)
    k = np.arange(6)
    axes[0].plot(k, stats.binom.pmf(k, 5, 0.5), 'o-', label='Exact PMF')
    axes[0].set(title='Binomial simulation', xlabel='Heads in 5 tosses', ylabel='Probability')
    axes[0].legend()
    axes[1].hist(group_a, alpha=0.55, label='Synthetic A')
    axes[1].hist(group_b, alpha=0.55, label='Synthetic B')
    axes[1].set(title='Welch t-test samples', xlabel='Value', ylabel='Count')
    axes[1].legend()
    axes[2].hist(means, bins=35, density=True)
    axes[2].axvline(2, color='black', linestyle='--', label='Population mean')
    axes[2].set(title='Central limit theorem', xlabel='Mean of 40 exponential draws', ylabel='Density')
    axes[2].legend()
    fig.tight_layout()
    fig.savefig(output / 'probability-and-inference.png', dpi=140)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
