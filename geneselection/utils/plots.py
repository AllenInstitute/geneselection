import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend("agg")

dpi = 100
figx = 6
figy = 4.5


def history(
    simple_logger,
    save_path,
    loss_name="recon_loss",
    do_not_print=["epoch", "iter", "time", "z"],
):

    # Figure out the default color order, and use these for the plots
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    plt.figure(figsize=(figx, figy), dpi=dpi)

    ax = plt.gca()

    plts = list()

    # Plot reconstruction loss
    plts += ax.plot(
        simple_logger.log["iter"],
        simple_logger.log[loss_name],
        label=loss_name,
        color=colors[0],
    )

    plt.ylabel(loss_name)

    ax_max = np.percentile(simple_logger.log[loss_name], 99)
    ax_min = np.percentile(simple_logger.log[loss_name], 0)

    ax.set_ylim([ax_min, ax_max])

    # Plot everything else that isn't below
    do_not_print += [loss_name]

    # Print off the reconLoss on it's own scale
    ax2 = plt.gca().twinx()

    y_vals = list()

    i = 1
    for field in simple_logger.log:
        if field not in do_not_print:
            plts += ax2.plot(
                simple_logger.log["iter"],
                simple_logger.log[field],
                label=field,
                color=colors[i],
            )
            y_vals += simple_logger.log[field]
            i += 1

    if i > 1:
        ax_max = np.percentile(np.hstack(y_vals), 99.5)
        ax_min = np.percentile(np.hstack(y_vals), 0)

        ax2.set_ylim([ax_min, ax_max])

        # Get all the labels for the legend from both axes
        labs = [l.get_label() for l in plts]

        # Print legend
        ax.legend(plts, labs)

    plt.ylabel("loss")
    plt.title("History")
    plt.xlabel("iteration")

    # Save
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
    plt.close()


def short_history(
    simple_logger, save_path, max_history_len=10000, loss_name="recon_loss"
):
    history = int(len(simple_logger.log["epoch"]) / 2)

    if history > max_history_len:
        history = max_history_len

    x = simple_logger.log["iter"][-history:]
    y = simple_logger.log[loss_name][-history:]

    epochs = np.floor(np.array(simple_logger.log["epoch"][-history:]))
    losses = np.array(simple_logger.log[loss_name][-history:])
    iters = np.array(simple_logger.log["iter"][-history:])
    uepochs = np.unique(epochs)

    epoch_losses = np.zeros(len(uepochs))
    epoch_iters = np.zeros(len(uepochs))
    i = 0
    for uepoch in uepochs:
        inds = np.equal(epochs, uepoch)
        loss = np.mean(losses[inds])
        epoch_losses[i] = loss
        epoch_iters[i] = np.mean(iters[inds])
        i += 1

    mval = np.mean(losses)

    plt.figure(figsize=(figx, figy), dpi=dpi)
    plt.plot(x, y, label=loss_name)
    plt.plot(epoch_iters, epoch_losses, color="darkorange", label="epoch avg")
    plt.plot(
        [np.min(iters), np.max(iters)],
        [mval, mval],
        color="darkorange",
        linestyle=":",
        label="window avg",
    )

    plt.legend()
    plt.title("Short history")
    plt.xlabel("iteration")
    plt.ylabel("loss")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
    plt.close()


# def embeddings(embedding, save_path):
#     plt.figure(figsize=(figx, figy), dpi=dpi)
#     colors = plt.get_cmap("plasma")(np.linspace(0, 1, embedding.shape[0]))
#     plt.scatter(embedding[:, 0], embedding[:, 1], s=2, color=colors)
#     plt.xlim([-4, 4])
#     plt.ylim([-4, 4])
#     plt.axis("equal")
#     plt.xlabel("z1")
#     plt.ylabel("z2")
#     plt.title("latent space embedding")

#     plt.tight_layout()
#     plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
#     plt.close()


# def embedding_variation(embedding_paths, figsize=(8, 4), save_path=None):

#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
#     colors = cm.viridis(np.linspace(0, 1, len(embedding_paths)))

#     for path, color in zip(embedding_paths, colors):
#         embeddings = pickle.load(open(path, "rb"))

#         var_dims = np.sort(np.var(embeddings, axis=0))[::-1]
#         ax1.plot(var_dims, color=color)
#         ax1.set_xlabel("dimension #")
#         ax1.set_ylabel("dimension variation")
#         ax1.set_ylim(0, 1.05)

#         ax2.plot(np.cumsum(var_dims) / np.sum(var_dims), color=color)
#         ax2.set_xlabel("dimension #")
#         ax2.set_ylabel("cumulative variation")

#     fig.tight_layout()

#     if save_path is not None:
#         plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
#         plt.close()
